#!/usr/bin/env python3
"""
Simple LinkedIn Viral Content Generator MCP Server for Railway
"""

import os
import json
import requests
import time
import re
from typing import Dict, Optional, Any, List
from pathlib import Path

from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
app = FastMCP("LinkedIn Viral Content Generator")

# Configuration
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_BASE_URL = "https://api.apify.com/v2"

# Knowledge base paths
KNOWLEDGE_BASE_DIR = Path(__file__).parent / "knowledge_base"
HOOKS_FILE = KNOWLEDGE_BASE_DIR / "hooks.md"
CONTENT_TEMPLATES_FILE = KNOWLEDGE_BASE_DIR / "content_templates.md"

# Global storage for workflow state
workflow_state = {
    "current_niche": None,
    "selected_platform": None,
    "discovered_content": [],
    "selected_content": None,
    "analyzed_data": {},
    "selected_hooks": [],
    "content_ideas": [],
    "generated_posts": []
}


def make_apify_request(actor_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Make a request to an Apify actor and wait for completion."""
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN environment variable is required")
    
    # Start the actor run
    run_url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs"
    headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
    
    response = requests.post(run_url, json=input_data, headers=headers)
    response.raise_for_status()
    
    run_data = response.json()
    run_id = run_data["data"]["id"]
    
    # Poll for completion
    status_url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs/{run_id}"
    max_wait = 300  # 5 minutes max
    wait_time = 0
    
    while wait_time < max_wait:
        status_response = requests.get(status_url, headers=headers)
        status_response.raise_for_status()
        status_data = status_response.json()
        
        if status_data["data"]["status"] == "SUCCEEDED":
            # Get the dataset items
            dataset_id = status_data["data"]["defaultDatasetId"]
            dataset_url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items"
            
            dataset_response = requests.get(dataset_url, headers=headers)
            dataset_response.raise_for_status()
            
            return {"status": "success", "data": dataset_response.json()}
        
        elif status_data["data"]["status"] in ["FAILED", "ABORTED", "TIMED-OUT"]:
            return {"status": "failed", "error": f"Actor run failed with status: {status_data['data']['status']}"}
        
        time.sleep(10)
        wait_time += 10
    
    return {"status": "failed", "error": "Actor run timed out"}


def load_knowledge_base() -> Dict[str, str]:
    """Load hook templates and content templates from knowledge base."""
    knowledge = {"hooks": "", "content_templates": ""}
    
    if HOOKS_FILE.exists():
        with open(HOOKS_FILE, "r", encoding="utf-8") as f:
            knowledge["hooks"] = f.read()
    
    if CONTENT_TEMPLATES_FILE.exists():
        with open(CONTENT_TEMPLATES_FILE, "r", encoding="utf-8") as f:
            knowledge["content_templates"] = f.read()
    
    return knowledge


@app.tool()
def start_content_discovery(niche: str, platform: str) -> str:
    """
    Start the content discovery process for a specific niche and platform.
    
    Args:
        niche: The topic/niche to research (e.g., "AI content creation tools")
        platform: The platform to scrape ("youtube", "tiktok", "instagram", "linkedin")
    
    Returns:
        Confirmation message with next steps
    """
    workflow_state["current_niche"] = niche
    workflow_state["selected_platform"] = platform.lower()
    
    return f"✅ Content discovery started for niche: '{niche}' on platform: '{platform}'\n\nNext: Use the appropriate scraping tool to discover content."


@app.tool()
def get_workflow_status() -> Dict[str, Any]:
    """
    Get the current status of the content generation workflow.
    
    Returns:
        Dictionary containing current workflow state and progress
    """
    return {
        "current_niche": workflow_state.get("current_niche"),
        "selected_platform": workflow_state.get("selected_platform"),
        "content_discovered": len(workflow_state.get("discovered_content", [])),
        "content_selected": workflow_state.get("selected_content") is not None,
        "data_analyzed": bool(workflow_state.get("analyzed_data")),
        "hooks_selected": bool(workflow_state.get("selected_hooks")),
        "ideas_generated": len(workflow_state.get("content_ideas", [])),
        "posts_generated": len(workflow_state.get("generated_posts", [])),
        "apify_token_configured": bool(APIFY_TOKEN),
        "knowledge_base_loaded": HOOKS_FILE.exists() and CONTENT_TEMPLATES_FILE.exists()
    }


# Add a simple health check
@app.tool()
def health_check() -> Dict[str, Any]:
    """Health check for the MCP server."""
    return {
        "status": "healthy",
        "server": "LinkedIn Viral Content Generator MCP Server",
        "apify_token_configured": bool(APIFY_TOKEN),
        "knowledge_base_loaded": HOOKS_FILE.exists() and CONTENT_TEMPLATES_FILE.exists(),
        "tools_available": 2  # start_content_discovery, get_workflow_status
    }


# Add a simple root endpoint for Railway health check
@app.custom_route("/", methods=["GET"])
def root_health_check(request):
    """Simple root endpoint for Railway health check."""
    return {
        "status": "healthy",
        "server": "LinkedIn Viral Content Generator MCP Server",
        "mcp_endpoint": "/mcp",
        "apify_configured": bool(APIFY_TOKEN)
    }


if __name__ == "__main__":
    # Simple server startup for Railway
    port = int(os.getenv("PORT", 8000))
    
    print(f"=== STARTING MCP SERVER ===")
    print(f"Port: {port}")
    print(f"Host: 0.0.0.0")
    print(f"APIFY_TOKEN configured: {bool(APIFY_TOKEN)}")
    print(f"Knowledge base loaded: {HOOKS_FILE.exists() and CONTENT_TEMPLATES_FILE.exists()}")
    print(f"Transport: http")
    print(f"Expected endpoint: /mcp")
    print(f"=== SERVER STARTING ===")
    
    try:
        # Use FastMCP's built-in server
        app.run(host="0.0.0.0", port=port, transport="http")
    except Exception as e:
        print(f"ERROR starting server: {e}")
        import traceback
        traceback.print_exc()
        raise
