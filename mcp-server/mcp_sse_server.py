#!/usr/bin/env python3
"""
Instagram Video Analyzer - MCP SSE Server
HTTP/SSE transport for online MCP access

This server exposes the MCP protocol over HTTP with Server-Sent Events (SSE)
allowing remote clients to connect and use MCP tools over the internet.
"""

import asyncio
import json
import logging
import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    CallToolResult,
    ListToolsResult,
    ListResourcesResult,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8100"))
API_KEYS = os.getenv("MCP_API_KEYS", "").split(",")  # Comma-separated API keys
REQUEST_TIMEOUT = 300.0

# In-memory session storage (use Redis in production)
active_sessions: Dict[str, Dict[str, Any]] = {}

# HTTP client
http_client: Optional[httpx.AsyncClient] = None


# ============================================================================
# AUTHENTICATION
# ============================================================================

class AuthToken(BaseModel):
    """API token for authentication"""
    token: str = Field(description="Bearer token for API authentication")


def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


async def verify_api_key(authorization: str = Header(None)) -> str:
    """Verify API key from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    token = authorization[7:]  # Remove "Bearer " prefix

    # Check if token is valid
    if API_KEYS and token not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return token


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global http_client

    logger.info("🚀 Starting MCP SSE Server...")

    # Initialize HTTP client
    http_client = httpx.AsyncClient(
        base_url=API_BASE_URL,
        timeout=httpx.Timeout(REQUEST_TIMEOUT),
        limits=httpx.Limits(max_connections=50, max_keepalive_connections=20)
    )

    # Test API connection
    try:
        response = await http_client.get("/health")
        if response.status_code == 200:
            logger.info(f"✅ Connected to backend API at {API_BASE_URL}")
        else:
            logger.warning(f"⚠️ Backend API responded with status {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to backend API: {e}")

    yield

    # Cleanup
    logger.info("🔄 Shutting down MCP SSE Server...")
    if http_client:
        await http_client.aclose()
    logger.info("✅ Server shutdown complete")


app = FastAPI(
    title="Instagram Video Analyzer MCP Server",
    description="MCP server with SSE transport for Instagram video analysis",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# MCP TOOL IMPLEMENTATIONS
# ============================================================================

async def analyze_video_tool(url: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
    """Analyze an Instagram video"""
    logger.info(f"🎬 Analyzing video: {url} (type: {analysis_type})")

    # Validate analysis type
    valid_types = ["comprehensive", "summary", "transcription", "visual_description"]
    if analysis_type not in valid_types:
        raise ValueError(f"Invalid analysis_type. Must be one of: {', '.join(valid_types)}")

    # Validate Instagram URL
    if not any(domain in url for domain in ["instagram.com", "instagr.am"]):
        raise ValueError("URL must be from Instagram")

    # Make API request
    payload = {
        "instagram_url": url,
        "analysis_type": analysis_type
    }

    response = await http_client.post("/api/video/analyze", json=payload)

    if response.status_code == 200:
        result = response.json()
        job_id = result.get("job_id")

        # Wait for completion
        logger.info(f"⏳ Waiting for analysis completion: {job_id}")
        final_result = await wait_for_completion(job_id)

        return {
            "success": True,
            "job_id": job_id,
            "status": "completed",
            "analysis": final_result
        }
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")


async def get_job_status_tool(job_id: str) -> Dict[str, Any]:
    """Get job status"""
    response = await http_client.get(f"/api/video/status/{job_id}")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")


async def list_recent_analyses_tool(limit: int = 10, page: int = 1) -> Dict[str, Any]:
    """List recent analyses"""
    params = {"per_page": limit, "page": page}
    response = await http_client.get("/api/jobs", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")


async def cancel_job_tool(job_id: str) -> Dict[str, Any]:
    """Cancel a job"""
    response = await http_client.post(f"/api/jobs/{job_id}/cancel")

    if response.status_code == 200:
        return {"success": True, "message": "Job cancelled successfully"}
    else:
        raise Exception(f"API error: {response.status_code}")


async def get_system_stats_tool() -> Dict[str, Any]:
    """Get system statistics"""
    response = await http_client.get("/api/jobs/stats")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")


async def wait_for_completion(job_id: str, max_wait: int = 300) -> Dict[str, Any]:
    """Wait for job completion"""
    waited = 0
    while waited < max_wait:
        response = await http_client.get(f"/api/video/status/{job_id}")

        if response.status_code == 200:
            status_data = response.json()
            status = status_data.get("status")

            if status == "completed":
                return status_data.get("analysis_result", {})
            elif status == "failed":
                error = status_data.get("error_message", "Unknown error")
                raise Exception(f"Analysis failed: {error}")

            await asyncio.sleep(5)
            waited += 5
        else:
            raise Exception(f"Status check error: {response.status_code}")

    raise Exception("Timeout waiting for analysis completion")


# ============================================================================
# MCP SERVER SETUP
# ============================================================================

def create_mcp_server() -> Server:
    """Create and configure MCP server"""
    server = Server("instagram-video-analyzer")

    # Register tools
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="analyze_instagram_video",
                description="Analyze an Instagram video using AI",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Instagram video URL"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["comprehensive", "summary", "transcription", "visual_description"],
                            "description": "Type of analysis",
                            "default": "comprehensive"
                        }
                    },
                    "required": ["url"]
                }
            ),
            Tool(
                name="get_job_status",
                description="Get the status of an analysis job",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type": "string",
                            "description": "Job ID to check"
                        }
                    },
                    "required": ["job_id"]
                }
            ),
            Tool(
                name="list_recent_analyses",
                description="List recent video analyses",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 10
                        },
                        "page": {
                            "type": "integer",
                            "description": "Page number",
                            "default": 1
                        }
                    }
                }
            ),
            Tool(
                name="cancel_job",
                description="Cancel a running analysis job",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type": "string",
                            "description": "Job ID to cancel"
                        }
                    },
                    "required": ["job_id"]
                }
            ),
            Tool(
                name="get_system_stats",
                description="Get system performance statistics",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls"""
        try:
            if name == "analyze_instagram_video":
                result = await analyze_video_tool(
                    arguments.get("url"),
                    arguments.get("analysis_type", "comprehensive")
                )
            elif name == "get_job_status":
                result = await get_job_status_tool(arguments.get("job_id"))
            elif name == "list_recent_analyses":
                result = await list_recent_analyses_tool(
                    arguments.get("limit", 10),
                    arguments.get("page", 1)
                )
            elif name == "cancel_job":
                result = await cancel_job_tool(arguments.get("job_id"))
            elif name == "get_system_stats":
                result = await get_system_stats_tool()
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )]

    return server


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Instagram Video Analyzer MCP Server",
        "version": "2.0.0",
        "transport": "SSE",
        "backend": API_BASE_URL,
        "endpoints": {
            "sse": "/sse",
            "health": "/health",
            "generate_key": "/generate-key"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    # Check backend connection
    backend_healthy = False
    try:
        response = await http_client.get("/health", timeout=5.0)
        backend_healthy = response.status_code == 200
    except:
        pass

    return {
        "status": "healthy" if backend_healthy else "degraded",
        "backend": "connected" if backend_healthy else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/generate-key")
async def generate_key(token: str = Depends(verify_api_key)):
    """Generate a new API key (admin only)"""
    new_key = generate_api_key()
    return {
        "api_key": new_key,
        "note": "Add this key to MCP_API_KEYS environment variable"
    }


@app.get("/sse")
async def sse_endpoint(
    request: Request,
    token: str = Depends(verify_api_key)
):
    """SSE endpoint for MCP protocol"""
    logger.info(f"🔌 New SSE connection from {request.client.host}")

    # Create MCP server instance
    mcp_server = create_mcp_server()

    # Create SSE transport
    async with SseServerTransport("/messages") as transport:
        # Session management
        session_id = secrets.token_urlsafe(16)
        active_sessions[session_id] = {
            "created_at": datetime.utcnow(),
            "client_ip": request.client.host
        }

        try:
            # Run MCP server with SSE transport
            async with transport.connect_sse(
                request.scope,
                lambda: None  # No special initialization needed
            ) as streams:
                await mcp_server.run(
                    streams[0],
                    streams[1],
                    mcp_server.create_initialization_options()
                )
        except Exception as e:
            logger.error(f"SSE connection error: {e}")
            raise
        finally:
            # Cleanup session
            if session_id in active_sessions:
                del active_sessions[session_id]
            logger.info(f"🔌 SSE connection closed")


@app.post("/messages")
async def messages_endpoint(
    request: Request,
    token: str = Depends(verify_api_key)
):
    """Message endpoint for MCP protocol"""
    body = await request.json()
    logger.debug(f"📨 Received message: {body}")

    # This endpoint is used by the SSE transport to send responses
    # The actual handling is done by the SSE connection
    return JSONResponse({"status": "received"})


@app.get("/sessions")
async def list_sessions(token: str = Depends(verify_api_key)):
    """List active sessions (admin only)"""
    return {
        "active_sessions": len(active_sessions),
        "sessions": [
            {
                "session_id": sid,
                "created_at": data["created_at"].isoformat(),
                "client_ip": data["client_ip"]
            }
            for sid, data in active_sessions.items()
        ]
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the MCP SSE server"""
    import uvicorn

    logger.info("🚀 Starting Instagram Video Analyzer MCP SSE Server")
    logger.info(f"📡 Backend API: {API_BASE_URL}")
    logger.info(f"🔒 Authentication: {'Enabled' if API_KEYS else 'Disabled (WARNING!)'}")
    logger.info(f"🌐 Server will listen on: http://0.0.0.0:{MCP_SERVER_PORT}")

    if not API_KEYS or API_KEYS == ['']:
        logger.warning("⚠️  WARNING: No API keys configured! Set MCP_API_KEYS environment variable")
        logger.warning("⚠️  Generate keys with: curl -X POST http://localhost:8100/generate-key")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=MCP_SERVER_PORT,
        log_level="info"
    )


if __name__ == "__main__":
    main()
