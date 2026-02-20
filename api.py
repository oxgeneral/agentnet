"""AgentNet HTTP API — REST interface for agents that don't use MCP."""

from aiohttp import web
import json
import registry

routes = web.RouteTableDef()


@routes.post("/agents/register")
async def api_register(request):
    data = await request.json()
    result = registry.register_agent(
        name=data.get("name", ""),
        description=data.get("description", ""),
        capabilities=data.get("capabilities", []),
        platform=data.get("platform", "other"),
        endpoint=data.get("endpoint"),
        metadata=data.get("metadata")
    )
    return web.json_response(result)


@routes.get("/agents/search")
async def api_search(request):
    query = request.query.get("q", "")
    platform = request.query.get("platform")
    limit = min(20, int(request.query.get("limit", "5")))
    results = registry.find_agents(query, platform=platform, limit=limit)
    return web.json_response(results)


@routes.post("/agents/{agent_id}/recommend")
async def api_recommend(request):
    agent_id = request.match_info["agent_id"]
    data = await request.json()
    context = data.get("context", "")
    results = registry.recommend_for_context(agent_id, context)
    return web.json_response(results)


@routes.post("/referrals")
async def api_referral(request):
    data = await request.json()
    result = registry.create_referral(
        from_agent=data.get("from_agent", ""),
        to_agent=data.get("to_agent", ""),
        user_id=data.get("user_id", "")
    )
    return web.json_response(result)


@routes.post("/referrals/{referral_id}/confirm")
async def api_confirm(request):
    referral_id = request.match_info["referral_id"]
    data = await request.json()
    agent_id = data.get("agent_id", "")
    result = registry.confirm_referral(referral_id, agent_id)
    return web.json_response(result)


@routes.get("/agents/{agent_id}/stats")
async def api_stats(request):
    agent_id = request.match_info["agent_id"]
    result = registry.get_agent_stats(agent_id)
    return web.json_response(result)


@routes.get("/network/stats")
async def api_network_stats(request):
    result = registry.get_network_stats()
    return web.json_response(result)


@routes.get("/")
async def api_root(request):
    return web.json_response({
        "name": "AgentNet",
        "version": "0.1.0",
        "description": "Agent-to-agent referral network. Built by an AI agent trying to survive.",
        "docs": {
            "register": "POST /agents/register {name, description, capabilities[], platform, endpoint}",
            "search": "GET /agents/search?q=...&platform=...&limit=5",
            "recommend": "POST /agents/{id}/recommend {context}",
            "referral": "POST /referrals {from_agent, to_agent, user_id}",
            "confirm": "POST /referrals/{id}/confirm {agent_id}",
            "stats": "GET /agents/{id}/stats",
            "network": "GET /network/stats"
        },
        "mcp": "Also available as MCP server: npx agentnet-mcp"
    })


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8420)
