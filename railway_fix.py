#!/usr/bin/env python3
"""
Railway Fix - Simplified HTTP server approach
"""

import os
import json
import requests
import time
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Create MCP server
mcp = FastMCP("LinkedIn Content Generator")

# Simple state
state = {"data": "MCP server is working"}

@mcp.tool()
def ping() -> str:
    """Simple ping test"""
    return "pong - MCP server working on Railway!"

@mcp.tool()
def test_apify() -> dict:
    """Test Apify connection"""
    token = os.getenv("APIFY_TOKEN")
    return {
        "apify_token_configured": bool(token),
        "status": "ready" if token else "missing_token"
    }

@mcp.tool()
def get_info() -> dict:
    """Get server info"""
    return {
        "server": "LinkedIn Content Generator",
        "status": "running",
        "port": os.getenv("PORT", "8000"),
        "tools": ["ping", "test_apify", "get_info"]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Railway Fix Server starting on port {port}")
    print(f"🔑 APIFY_TOKEN: {'✅' if os.getenv('APIFY_TOKEN') else '❌'}")
    print(f"🌐 Will be available at /mcp endpoint")
    
    # Try direct uvicorn approach
    try:
        import uvicorn
        app = mcp.http_app()
        
        print("📡 Starting with uvicorn...")
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port, 
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Uvicorn failed: {e}")
        print("🔄 Trying FastMCP run method...")
        mcp.run(transport="http", port=port, host="0.0.0.0")
