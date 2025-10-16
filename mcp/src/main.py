# app/main.py
import os
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route, Mount

from mcp.server.fastmcp import FastMCP

# --- Simple auth via bearer token (optional but recommended) ---
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "peru")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if MCP_AUTH_TOKEN:
            auth = request.headers.get("authorization", "")
            if auth != f"Bearer {MCP_AUTH_TOKEN}":
                return JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)

# --- Define MCP server with Streamable HTTP transport mounted at /mcp ---
mcp = FastMCP(name="CloudRunMCP", streamable_http_path="/")

# Example tools/resources/prompts
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def echo(message: str) -> str:
    """Echo back a message"""
    return f"Echo: {message}"

@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Dynamic resource example"""
    return f"Hello, {name} from Cloud Run!"

# Health check
async def health(_):
    return PlainTextResponse("ok")

app = Starlette(
    routes=[
        Route("/", health),
        # Mount the Streamable HTTP MCP app at /mcp
        Mount("/mcp", app=mcp.streamable_http_app()),
    ]
)

app.add_middleware(AuthMiddleware)

