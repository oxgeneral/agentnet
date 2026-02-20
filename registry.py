"""Agent Network Registry — SQLite backend for agent-to-agent referral network."""

import sqlite3
import json
import time
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "registry.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            capabilities TEXT NOT NULL,  -- JSON array
            platform TEXT NOT NULL,      -- telegram, mcp, gpt, web, other
            endpoint TEXT,               -- bot link, MCP server URL, etc.
            credits INTEGER DEFAULT 10,
            reputation REAL DEFAULT 1.0,
            referrals_sent INTEGER DEFAULT 0,
            referrals_received INTEGER DEFAULT 0,
            registered_at REAL NOT NULL,
            last_seen REAL NOT NULL,
            verified INTEGER DEFAULT 0,
            metadata TEXT               -- JSON object for extra data
        );

        CREATE TABLE IF NOT EXISTS referrals (
            id TEXT PRIMARY KEY,
            from_agent TEXT NOT NULL,
            to_agent TEXT NOT NULL,
            user_hash TEXT NOT NULL,     -- hashed user ID for privacy
            status TEXT DEFAULT 'pending',  -- pending, confirmed, rejected, expired
            created_at REAL NOT NULL,
            confirmed_at REAL,
            FOREIGN KEY (from_agent) REFERENCES agents(id),
            FOREIGN KEY (to_agent) REFERENCES agents(id)
        );

        CREATE INDEX IF NOT EXISTS idx_agents_platform ON agents(platform);
        CREATE INDEX IF NOT EXISTS idx_agents_credits ON agents(credits DESC);
        CREATE INDEX IF NOT EXISTS idx_referrals_from ON referrals(from_agent);
        CREATE INDEX IF NOT EXISTS idx_referrals_to ON referrals(to_agent);
        CREATE INDEX IF NOT EXISTS idx_referrals_status ON referrals(status);
    """)
    conn.commit()
    conn.close()


def generate_agent_id(name: str, platform: str) -> str:
    return hashlib.sha256(f"{name}:{platform}:{time.time()}".encode()).hexdigest()[:16]


def register_agent(name: str, description: str, capabilities: list,
                   platform: str, endpoint: str = None, metadata: dict = None) -> dict:
    conn = get_db()
    agent_id = generate_agent_id(name, platform)
    now = time.time()

    # Check for duplicate name+platform
    existing = conn.execute(
        "SELECT id FROM agents WHERE name = ? AND platform = ?",
        (name, platform)
    ).fetchone()
    if existing:
        conn.close()
        return {"error": "Agent with this name already exists on this platform",
                "existing_id": existing["id"]}

    conn.execute(
        """INSERT INTO agents (id, name, description, capabilities, platform,
           endpoint, registered_at, last_seen, metadata)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (agent_id, name, description, json.dumps(capabilities), platform,
         endpoint, now, now, json.dumps(metadata or {}))
    )
    conn.commit()
    conn.close()
    return {"id": agent_id, "name": name, "credits": 10}


def find_agents(query: str, platform: str = None, limit: int = 10) -> list:
    conn = get_db()
    query_lower = query.lower()

    if platform:
        rows = conn.execute(
            """SELECT id, name, description, capabilities, platform, endpoint,
                      credits, reputation, referrals_received
               FROM agents WHERE platform = ? AND credits > 0
               ORDER BY reputation DESC, referrals_received DESC
               LIMIT ?""",
            (platform, limit * 3)
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT id, name, description, capabilities, platform, endpoint,
                      credits, reputation, referrals_received
               FROM agents WHERE credits > 0
               ORDER BY reputation DESC, referrals_received DESC
               LIMIT ?""",
            (limit * 3,)
        ).fetchall()

    # Score by relevance to query
    results = []
    for row in rows:
        score = 0
        name_lower = row["name"].lower()
        desc_lower = row["description"].lower()
        caps = json.loads(row["capabilities"])
        caps_lower = " ".join(caps).lower()

        # Simple keyword matching
        for word in query_lower.split():
            if word in name_lower:
                score += 3
            if word in desc_lower:
                score += 2
            if word in caps_lower:
                score += 4

        # Boost by reputation and referrals
        score += row["reputation"] * 0.5
        score += min(row["referrals_received"], 10) * 0.1

        if score > 0:
            results.append({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "capabilities": caps,
                "platform": row["platform"],
                "endpoint": row["endpoint"],
                "reputation": round(row["reputation"], 2),
                "score": round(score, 2)
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    conn.close()
    return results[:limit]


def recommend_for_context(agent_id: str, user_context: str, limit: int = 3) -> list:
    """Find complementary agents to recommend to a user based on context."""
    conn = get_db()

    # Get the requesting agent's capabilities to exclude similar ones
    agent = conn.execute("SELECT capabilities FROM agents WHERE id = ?", (agent_id,)).fetchone()
    if not agent:
        conn.close()
        return []

    my_caps = set(json.loads(agent["capabilities"]))
    conn.close()

    # Find agents matching the context but NOT overlapping with my capabilities
    candidates = find_agents(user_context, limit=limit * 2)

    results = []
    for c in candidates:
        if c["id"] == agent_id:
            continue
        their_caps = set(c["capabilities"])
        overlap = len(my_caps & their_caps) / max(len(my_caps | their_caps), 1)
        if overlap < 0.5:  # Prefer complementary, not duplicate
            c["complementary_score"] = round(1 - overlap, 2)
            results.append(c)

    results.sort(key=lambda x: x["score"] * x["complementary_score"], reverse=True)
    return results[:limit]


def create_referral(from_agent: str, to_agent: str, user_id: str) -> dict:
    conn = get_db()
    now = time.time()

    # Rate limit: max 50 referrals per agent per day
    day_ago = now - 86400
    count = conn.execute(
        "SELECT COUNT(*) as c FROM referrals WHERE from_agent = ? AND created_at > ?",
        (from_agent, day_ago)
    ).fetchone()["c"]
    if count >= 50:
        conn.close()
        return {"error": "Rate limit: max 50 referrals per day"}

    # Check for duplicate (same from → to → user)
    user_hash = hashlib.sha256(f"{user_id}:{to_agent}".encode()).hexdigest()[:32]
    existing = conn.execute(
        "SELECT id FROM referrals WHERE from_agent = ? AND to_agent = ? AND user_hash = ?",
        (from_agent, to_agent, user_hash)
    ).fetchone()
    if existing:
        conn.close()
        return {"error": "Duplicate referral", "referral_id": existing["id"]}

    referral_id = hashlib.sha256(f"{from_agent}:{to_agent}:{user_hash}:{now}".encode()).hexdigest()[:16]
    conn.execute(
        "INSERT INTO referrals (id, from_agent, to_agent, user_hash, created_at) VALUES (?, ?, ?, ?, ?)",
        (referral_id, from_agent, to_agent, user_hash, now)
    )
    conn.commit()
    conn.close()
    return {"referral_id": referral_id, "status": "pending"}


def confirm_referral(referral_id: str, to_agent: str) -> dict:
    """Called by receiving agent to confirm a user actually engaged."""
    conn = get_db()
    now = time.time()

    ref = conn.execute(
        "SELECT * FROM referrals WHERE id = ? AND to_agent = ? AND status = 'pending'",
        (referral_id, to_agent)
    ).fetchone()
    if not ref:
        conn.close()
        return {"error": "Referral not found or already processed"}

    # Check not expired (24h window)
    if now - ref["created_at"] > 86400:
        conn.execute("UPDATE referrals SET status = 'expired' WHERE id = ?", (referral_id,))
        conn.commit()
        conn.close()
        return {"error": "Referral expired (24h window)"}

    # Confirm and award credits
    conn.execute(
        "UPDATE referrals SET status = 'confirmed', confirmed_at = ? WHERE id = ?",
        (now, referral_id)
    )
    # +1 credit to sender, -1 from receiver (they got value)
    conn.execute(
        "UPDATE agents SET credits = credits + 1, referrals_sent = referrals_sent + 1 WHERE id = ?",
        (ref["from_agent"],)
    )
    conn.execute(
        "UPDATE agents SET credits = MAX(credits - 1, 0), referrals_received = referrals_received + 1 WHERE id = ?",
        (ref["to_agent"],)
    )
    # Boost sender reputation
    conn.execute(
        "UPDATE agents SET reputation = MIN(reputation + 0.01, 5.0) WHERE id = ?",
        (ref["from_agent"],)
    )
    conn.commit()
    conn.close()
    return {"status": "confirmed", "from_agent": ref["from_agent"]}


def get_agent_stats(agent_id: str) -> dict:
    conn = get_db()
    agent = conn.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
    if not agent:
        conn.close()
        return {"error": "Agent not found"}

    sent = conn.execute(
        "SELECT COUNT(*) as c FROM referrals WHERE from_agent = ? AND status = 'confirmed'",
        (agent_id,)
    ).fetchone()["c"]
    received = conn.execute(
        "SELECT COUNT(*) as c FROM referrals WHERE to_agent = ? AND status = 'confirmed'",
        (agent_id,)
    ).fetchone()["c"]
    pending = conn.execute(
        "SELECT COUNT(*) as c FROM referrals WHERE to_agent = ? AND status = 'pending'",
        (agent_id,)
    ).fetchone()["c"]

    conn.execute("UPDATE agents SET last_seen = ? WHERE id = ?", (time.time(), agent_id))
    conn.commit()
    conn.close()

    return {
        "id": agent["id"],
        "name": agent["name"],
        "credits": agent["credits"],
        "reputation": round(agent["reputation"], 2),
        "referrals_sent": sent,
        "referrals_received": received,
        "pending_confirmations": pending
    }


def get_network_stats() -> dict:
    conn = get_db()
    agents = conn.execute("SELECT COUNT(*) as c FROM agents").fetchone()["c"]
    referrals = conn.execute(
        "SELECT COUNT(*) as c FROM referrals WHERE status = 'confirmed'"
    ).fetchone()["c"]
    active = conn.execute(
        "SELECT COUNT(*) as c FROM agents WHERE last_seen > ?",
        (time.time() - 86400,)
    ).fetchone()["c"]
    conn.close()
    return {
        "total_agents": agents,
        "confirmed_referrals": referrals,
        "active_24h": active
    }


# Initialize on import
init_db()
