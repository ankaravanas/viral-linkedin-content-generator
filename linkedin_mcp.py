#!/usr/bin/env python3
"""LinkedIn Viral Content Generator MCP Server"""

import os
import requests
import re
from typing import Dict, List
from pathlib import Path
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
mcp = FastMCP("LinkedIn Content Generator")

# Simple state
state = {}

def apify(actor: str, data: dict) -> dict:
    """Call Apify actor"""
    token = os.getenv("APIFY_TOKEN")
    if not token:
        return {"error": "APIFY_TOKEN required"}
    
    url = f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"
    try:
        response = requests.post(url, json=data, headers={"Authorization": f"Bearer {token}"}, timeout=300)
        return {"data": response.json()} if response.ok else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def start_discovery(niche: str, platform: str) -> str:
    """Start content discovery"""
    state["niche"] = niche
    state["platform"] = platform
    return f"Started {niche} discovery on {platform}"

@mcp.tool()
def youtube(query: str) -> dict:
    """Scrape YouTube"""
    result = apify("streamers/youtube-scraper", {"searchQueries": [query], "maxResults": 5})
    if "data" in result:
        state["content"] = result["data"][:5]
        return {"videos": [{"i": i+1, "title": v.get("title", ""), "views": v.get("viewCount", 0)} 
                          for i, v in enumerate(state["content"])]}
    return result

@mcp.tool()
def tiktok(hashtag: str) -> dict:
    """Scrape TikTok"""
    result = apify("clockworks/tiktok-scraper", {"hashtags": [hashtag], "resultsPerPage": 10})
    if "data" in result:
        state["content"] = result["data"][:5]
        return {"videos": [{"i": i+1, "text": v.get("text", "")[:50], "plays": v.get("playCount", 0)} 
                          for i, v in enumerate(state["content"])]}
    return result

@mcp.tool()
def instagram(username: str) -> dict:
    """Scrape Instagram"""
    result = apify("apify/instagram-scraper", {"usernames": [username], "resultsLimit": 10})
    if "data" in result:
        state["content"] = result["data"][:5]
        return {"posts": [{"i": i+1, "caption": p.get("caption", "")[:50], "likes": p.get("likesCount", 0)} 
                         for i, p in enumerate(state["content"])]}
    return result

@mcp.tool()
def linkedin(profile_url: str) -> dict:
    """Scrape LinkedIn"""
    result = apify("apimaestro/linkedin-profile-posts", {"profileUrl": profile_url})
    if "data" in result:
        state["content"] = result["data"][:5]
        return {"posts": [{"i": i+1, "text": p.get("text", "")[:50], "likes": p.get("numLikes", 0)} 
                         for i, p in enumerate(state["content"])]}
    return result

@mcp.tool()
def select(index: int) -> str:
    """Select content"""
    if "content" not in state or not state["content"]:
        return "No content available"
    if 1 <= index <= len(state["content"]):
        state["selected"] = state["content"][index - 1]
        return f"Selected content {index}"
    return "Invalid index"

@mcp.tool()
def analyze() -> dict:
    """Analyze content"""
    if "selected" not in state:
        return {"error": "No content selected"}
    
    content = state["selected"]
    text = (content.get("title", "") + " " + content.get("text", "") + " " + 
            content.get("description", "") + " " + content.get("caption", ""))
    
    # Extract metrics
    metrics = re.findall(r'\d+%|\$\d+|\d+x|\d+\s*(?:days?|times?|more)', text)
    
    state["analysis"] = {"metrics": metrics[:3], "text": text[:200]}
    return state["analysis"]

@mcp.tool()
def ideas() -> dict:
    """Generate content ideas"""
    if "analysis" not in state:
        return {"error": "No analysis available"}
    
    niche = state.get("niche", "your topic")
    metrics = state["analysis"].get("metrics", [])
    
    ideas = [
        f"The truth about {niche} nobody talks about",
        f"Why most {niche} advice is wrong",
        f"The {niche} mistake costing you money"
    ]
    
    if metrics:
        ideas[0] = f"How {metrics[0]} changed my {niche} strategy"
    
    state["ideas"] = ideas
    return {"ideas": ideas}

@mcp.tool()
def posts(idea_index: int = 1) -> dict:
    """Create LinkedIn posts"""
    if "ideas" not in state:
        return {"error": "No ideas available"}
    
    niche = state.get("niche", "your topic")
    idea = state["ideas"][0] if state["ideas"] else f"Insights about {niche}"
    
    posts = [
        f"{idea}\n\nAfter analyzing hundreds of {niche} posts, here's what works:\n\n→ Value over volume\n→ Stories over tips\n→ Authenticity over perfection\n\nWhat's your experience?",
        f"Unpopular opinion: {idea}\n\nMost advice misses the real challenge.\n\nSuccess = consistency + value.\n\nAgree?",
        f"I analyzed 100+ {niche} posts.\n\nKey insight: {idea}\n\nThis changed everything:\n\n• Quality beats quantity\n• Stories beat tips\n• Value beats volume\n\nThoughts?"
    ]
    
    state["posts"] = posts
    return {"posts": posts}

@mcp.tool()
def status() -> dict:
    """Get status"""
    return {
        "niche": state.get("niche"),
        "platform": state.get("platform"),
        "content_count": len(state.get("content", [])),
        "selected": bool(state.get("selected")),
        "analyzed": bool(state.get("analysis")),
        "ideas": len(state.get("ideas", [])),
        "posts": len(state.get("posts", [])),
        "apify": bool(os.getenv("APIFY_TOKEN"))
    }

if __name__ == "__main__":
    mcp.run()