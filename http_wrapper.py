#!/usr/bin/env python3
"""
HTTP Wrapper for LinkedIn Viral Content Generator MCP Server

This is a simple HTTP wrapper to test that the server is deployed correctly on Railway.
The actual MCP server uses stdio transport and should be connected via MCP clients.
"""

import os
from flask import Flask, jsonify
from server import mcp, workflow_state, load_knowledge_base

app = Flask(__name__)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "LinkedIn Viral Content Generator MCP Server",
        "note": "This is an MCP server. Connect via MCP clients, not HTTP.",
        "tools_available": len(mcp.tools),
        "knowledge_base_loaded": {
            "hooks_file_exists": os.path.exists("knowledge_base/hooks.md"),
            "content_templates_file_exists": os.path.exists("knowledge_base/content_templates.md")
        }
    })

@app.route('/health')
def health():
    """Health check for Railway"""
    try:
        # Test knowledge base loading
        knowledge = load_knowledge_base()
        
        return jsonify({
            "status": "healthy",
            "apify_token_configured": bool(os.getenv("APIFY_TOKEN")),
            "knowledge_base": {
                "hooks_loaded": len(knowledge.get("hooks", "")) > 100,
                "content_templates_loaded": len(knowledge.get("content_templates", "")) > 100
            },
            "mcp_tools": list(mcp.tools.keys())
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/mcp')
def mcp_info():
    """Information about MCP connection"""
    return jsonify({
        "message": "This is an MCP (Model Context Protocol) server",
        "connection_method": "stdio transport",
        "note": "Cannot be accessed via HTTP URLs",
        "how_to_connect": {
            "local": {
                "command": "python",
                "args": ["server.py"],
                "env": {"APIFY_TOKEN": "your_token"}
            },
            "claude_desktop_config": {
                "mcpServers": {
                    "viral-linkedin-content-generator": {
                        "command": "python",
                        "args": ["path/to/server.py"],
                        "env": {"APIFY_TOKEN": "your_token"}
                    }
                }
            }
        },
        "available_tools": list(mcp.tools.keys())
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
