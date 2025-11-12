#!/usr/bin/env python3
"""Test script to validate Apify actor IDs and API calls"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_actor_exists(actor_id: str) -> dict:
    """Test if an Apify actor exists"""
    token = os.getenv("APIFY_TOKEN")
    if not token or token == "your_apify_token_here":
        return {"error": "APIFY_TOKEN not configured"}
    
    # Check if actor exists
    url = f"https://api.apify.com/v2/acts/{actor_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            actor_data = response.json()
            return {
                "status": "exists",
                "name": actor_data["data"]["name"],
                "description": actor_data["data"]["description"][:100]
            }
        elif response.status_code == 404:
            return {"status": "not_found", "error": "Actor not found"}
        else:
            return {"status": "error", "code": response.status_code, "error": response.text[:200]}
            
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    actors_to_test = [
        "streamers/youtube-scraper",
        "clockworks/tiktok-scraper", 
        "apify/instagram-scraper",
        "apimaestro/linkedin-profile-posts",
        "streamers/youtube-comments-scraper",
        "clockworks/tiktok-comments-scraper",
        "apify/instagram-comment-scraper",
        "apimaestro/linkedin-post-comments-replies-engagements-scraper-no-cookies"
    ]
    
    print("🧪 Testing Apify actor IDs...")
    print(f"Token configured: {bool(os.getenv('APIFY_TOKEN'))}")
    print()
    
    for actor in actors_to_test:
        result = test_actor_exists(actor)
        status = result.get("status", "unknown")
        
        if status == "exists":
            print(f"✅ {actor} - EXISTS: {result['name']}")
        elif status == "not_found":
            print(f"❌ {actor} - NOT FOUND")
        else:
            print(f"⚠️  {actor} - ERROR: {result.get('error', 'Unknown')[:100]}")
    
    print("\nActor validation completed.")
