#!/usr/bin/env python3
"""
LinkedIn Viral Content Generator MCP Server - LEAN VERSION
"""

import os
import json
import requests
import time
import re
from typing import Dict, List, Optional, Any
from pathlib import Path
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Create MCP server
mcp = FastMCP("LinkedIn Content Generator")

# Global state
state = {
    "niche": None,
    "platform": None,
    "content": [],
    "selected": None,
    "analysis": {},
    "hooks": [],
    "ideas": [],
    "posts": []
}

def apify_request(actor: str, data: dict) -> dict:
    """Make Apify API request"""
    token = os.getenv("APIFY_TOKEN")
    if not token:
        return {"error": "APIFY_TOKEN not set"}
    
    url = f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=300)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def start_discovery(niche: str, platform: str) -> str:
    """Start content discovery"""
    state["niche"] = niche
    state["platform"] = platform.lower()
    return f"Started discovery for {niche} on {platform}"

@mcp.tool()
def scrape_youtube(query: str) -> dict:
    """Scrape YouTube videos"""
    result = apify_request("streamers/youtube-scraper", {
        "searchQueries": [query],
        "maxResults": 5,
        "downloadSubtitles": True
    })
    
    if result.get("success"):
        state["content"] = result["data"][:5]
        videos = []
        for i, video in enumerate(state["content"], 1):
            videos.append({
                "index": i,
                "title": video.get("title", ""),
                "url": video.get("url", ""),
                "views": video.get("viewCount", 0)
            })
        return {"videos": videos}
    
    return result

@mcp.tool()
def scrape_tiktok(hashtag: str) -> dict:
    """Scrape TikTok videos"""
    result = apify_request("clockworks/tiktok-scraper", {
        "hashtags": [hashtag],
        "resultsPerPage": 10
    })
    
    if result.get("success"):
        state["content"] = result["data"][:5]
        videos = []
        for i, video in enumerate(state["content"], 1):
            videos.append({
                "index": i,
                "text": video.get("text", "")[:100],
                "plays": video.get("playCount", 0),
                "likes": video.get("diggCount", 0)
            })
        return {"videos": videos}
    
    return result

@mcp.tool()
def select_content(index: int) -> str:
    """Select content by index"""
    if not state["content"]:
        return "No content available"
    
    if 1 <= index <= len(state["content"]):
        state["selected"] = state["content"][index - 1]
        return f"Selected content {index}"
    
    return "Invalid index"

@mcp.tool()
def analyze_content() -> dict:
    """Analyze selected content"""
    if not state["selected"]:
        return {"error": "No content selected"}
    
    # Simple analysis
    content = state["selected"]
    text = content.get("title", "") + " " + content.get("text", "") + " " + content.get("description", "")
    
    # Extract metrics
    metrics = re.findall(r'\d+%|\$\d+|\d+x', text)
    
    state["analysis"] = {
        "metrics": metrics[:3],
        "text_length": len(text),
        "platform": state["platform"]
    }
    
    return state["analysis"]

@mcp.tool()
def generate_ideas() -> dict:
    """Generate content ideas"""
    if not state["analysis"]:
        return {"error": "No analysis available"}
    
    niche = state["niche"] or "your topic"
    metrics = state["analysis"].get("metrics", [])
    
    ideas = [
        f"The truth about {niche} that nobody talks about",
        f"Why most {niche} advice is wrong",
        f"The {niche} mistake costing you money"
    ]
    
    if metrics:
        ideas.append(f"How {metrics[0]} changed my {niche} strategy")
    
    state["ideas"] = ideas
    return {"ideas": ideas}

@mcp.tool()
def create_posts() -> dict:
    """Create LinkedIn posts"""
    if not state["ideas"]:
        return {"error": "No ideas available"}
    
    niche = state["niche"] or "your topic"
    idea = state["ideas"][0]
    
    posts = [
        f"{idea}\n\nAfter analyzing hundreds of {niche} posts, I discovered something shocking.\n\nMost people are doing it completely wrong.\n\nHere's what actually works:\n\n→ Focus on value, not volume\n→ Tell stories, don't just share tips\n→ Engage authentically\n\nWhat's your experience with {niche}?",
        
        f"Unpopular opinion about {niche}:\n\n{idea}\n\nEveryone talks about best practices, but nobody mentions the real challenges.\n\nThe truth? Success comes from consistency, not perfection.\n\nAgree or disagree?",
        
        f"Last week I analyzed 100+ {niche} posts.\n\nThe results were eye-opening.\n\n{idea}\n\nThis completely changed my approach.\n\nHere's what I learned:\n\n• Quality beats quantity every time\n• Authentic stories outperform generic tips\n• Engagement is about genuine connection\n\nWhat's worked for you?"
    ]
    
    state["posts"] = posts
    return {"posts": posts}

@mcp.tool()
def get_status() -> dict:
    """Get workflow status"""
    return {
        "niche": state["niche"],
        "platform": state["platform"],
        "content_count": len(state["content"]),
        "has_selection": bool(state["selected"]),
        "has_analysis": bool(state["analysis"]),
        "ideas_count": len(state["ideas"]),
        "posts_count": len(state["posts"]),
        "apify_configured": bool(os.getenv("APIFY_TOKEN"))
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting MCP server on port {port}")
    
    if os.getenv("PORT"):
        # Railway deployment - use HTTP transport
        mcp.run(transport="http", port=port, host="0.0.0.0")
    else:
        # Local development - use stdio
        mcp.run()
