"""AgentNet MCP Server — Streamable HTTP transport for remote access."""

import uvicorn
from server import mcp

app = mcp.streamable_http_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8421)
