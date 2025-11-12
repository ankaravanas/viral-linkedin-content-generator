#!/usr/bin/env python3
"""
Ultra-simple MCP server for Railway deployment
"""

import os
from fastmcp import FastMCP

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize FastMCP server
app = FastMCP("LinkedIn Content Generator")

@app.tool()
def ping() -> str:
    """Simple ping tool to test MCP server is working."""
    return "pong - MCP server is working!"

@app.tool() 
def get_status() -> dict:
    """Get server status."""
    return {
        "status": "healthy",
        "server": "LinkedIn Content Generator MCP Server",
        "apify_configured": bool(os.getenv("APIFY_TOKEN"))
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting simple MCP server on port {port}")
    
    # Start the server
    app.run(host="0.0.0.0", port=port, transport="http")
