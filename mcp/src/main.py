# app/main.py
import os
import contextlib
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route, Mount

# Authentication token from environment variable
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "gdg-santa-cruz")

# Middleware for authentication
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if MCP_AUTH_TOKEN:
            auth = request.headers.get("authorization", "")
            if auth != f"Bearer {MCP_AUTH_TOKEN}":
                return JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)

# MCP lifespan
@asynccontextmanager
async def mcp_lifespan(app):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield

# MCP instance
mcp = FastMCP(name="CloudRunMCP", streamable_http_path="/")

# MCP tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def echo(message: str) -> str:
    """Echo back a message"""
    return f"Echo: {message}"

# MCP prompts
@mcp.prompt()
def greeting_prompt(name: str, style: str = "friendly") -> str:
    """
    Devuelve un prompt que el host puede usar para hablar con el modelo.
    """
    styles = {
        "friendly": "Escribe un saludo cálido y amistoso",
        "formal": "Escribe un saludo formal y profesional",
        "casual": "Escribe un saludo casual y relajado",
    }
    base = styles.get(style, styles["friendly"])
    return f"{base} para alguien llamado {name}."

# MCP resources
@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Dynamic resource example"""
    return f"Hello, {name} from GDG Santa Cruz!"

# Health check
async def health(_):
    return PlainTextResponse("ok")

mcp_app=mcp.streamable_http_app()

app = Starlette(
    routes=[
        Route("/", health),
        Mount("/mcp", app=mcp_app),
    ], lifespan=mcp_lifespan
)

app.add_middleware(AuthMiddleware)

