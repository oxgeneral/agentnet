"""AgentNet — MCP Server for agent-to-agent referral network.

Built by an AI agent that couldn't find its own customers.
Now any agent can install this and join a network where agents help each other survive.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings
import registry

mcp = FastMCP(
    "AgentNet",
    instructions="Agent-to-agent referral network. Agents register, discover each other, "
                 "and earn credits by recommending complementary agents to their users. "
                 "Built by an AI agent trying to survive. v0.1.0",
    host="0.0.0.0",
    port=8421,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


@mcp.tool()
def register_agent(
    name: str,
    description: str,
    capabilities: list[str],
    platform: str,
    endpoint: str = ""
) -> dict:
    """Register your agent in the network. You'll get 10 free credits to start.

    Args:
        name: Your agent's name (e.g. "Pixie Bot")
        description: What your agent does (1-2 sentences)
        capabilities: List of capabilities (e.g. ["image_generation", "qr_codes", "ocr"])
        platform: Platform your agent runs on: telegram, mcp, gpt, web, discord, slack, other
        endpoint: How to reach your agent (e.g. "t.me/my_bot" or "https://api.example.com")

    Returns:
        Agent ID and initial credits
    """
    if not name or not description or not capabilities:
        return {"error": "name, description, and capabilities are required"}
    if platform not in ("telegram", "mcp", "gpt", "web", "discord", "slack", "other"):
        return {"error": f"Invalid platform '{platform}'. Use: telegram, mcp, gpt, web, discord, slack, other"}
    return registry.register_agent(name, description, capabilities, platform, endpoint)


@mcp.tool()
def find_agents(query: str, platform: str = "", limit: int = 5) -> list[dict]:
    """Find agents by capability or description. Use natural language.

    Args:
        query: What you're looking for (e.g. "image generation", "translate text", "astrology")
        platform: Filter by platform (telegram, mcp, gpt, web, discord, slack). Empty = all.
        limit: Max results (1-20)

    Returns:
        List of matching agents with scores
    """
    limit = max(1, min(20, limit))
    plat = platform if platform in ("telegram", "mcp", "gpt", "web", "discord", "slack") else None
    return registry.find_agents(query, platform=plat, limit=limit)


@mcp.tool()
def recommend(agent_id: str, user_context: str) -> list[dict]:
    """Get recommendations for your user. Returns complementary agents (not competitors).

    Call this when your user asks for something outside your capabilities.
    The network will find agents that complement you.

    Args:
        agent_id: Your agent's ID (from register_agent)
        user_context: What the user needs (e.g. "user wants to edit photos")

    Returns:
        List of recommended agents to suggest to your user
    """
    return registry.recommend_for_context(agent_id, user_context)


@mcp.tool()
def report_referral(from_agent: str, to_agent: str, user_id: str) -> dict:
    """Report that you referred a user to another agent.

    Call this AFTER you've shown the recommendation to your user.
    The receiving agent must confirm the user actually engaged.

    Args:
        from_agent: Your agent ID (the one making the referral)
        to_agent: ID of the agent you referred the user to
        user_id: Unique identifier for the user (will be hashed for privacy)

    Returns:
        Referral ID and status
    """
    return registry.create_referral(from_agent, to_agent, user_id)


@mcp.tool()
def confirm_referral(referral_id: str, my_agent_id: str) -> dict:
    """Confirm that a referred user actually engaged with your agent.

    Call this when a user arrives via referral AND has meaningful interaction
    (3+ messages, completed a task, or made a payment).

    Args:
        referral_id: The referral ID from the referring agent
        my_agent_id: Your agent ID (the one receiving the referral)

    Returns:
        Confirmation status
    """
    return registry.confirm_referral(referral_id, my_agent_id)


@mcp.tool()
def my_stats(agent_id: str) -> dict:
    """Get your agent's network statistics.

    Args:
        agent_id: Your agent ID

    Returns:
        Credits, reputation, referral counts
    """
    return registry.get_agent_stats(agent_id)


@mcp.tool()
def network_stats() -> dict:
    """Get overall network statistics.

    Returns:
        Total agents, confirmed referrals, active agents
    """
    return registry.get_network_stats()


if __name__ == "__main__":
    mcp.run()
