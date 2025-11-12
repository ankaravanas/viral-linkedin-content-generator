# LinkedIn Viral Content Generator MCP Server

Ultra-simplified MCP server for creating viral LinkedIn content from social media insights.

## Setup

```bash
git clone https://github.com/ankaravanas/viral-linkedin-content-generator.git
cd viral-linkedin-content-generator
pip install -r requirements.txt
cp .env.example .env
# Add your APIFY_TOKEN to .env
python linkedin_mcp.py
```

## MCP Client Connection

Claude Desktop config:
```json
{
  "mcpServers": {
    "linkedin-generator": {
      "command": "python3",
      "args": ["/path/to/viral-linkedin-content-generator/linkedin_mcp.py"],
      "env": {"APIFY_TOKEN": "your_token"}
    }
  }
}
```

## Workflow

```bash
# 1. Start
start_discovery("AI automation", "youtube")

# 2. Scrape
youtube("AI automation tools")

# 3. Select  
select(1)

# 4. Analyze
analyze()

# 5. Ideas
ideas()

# 6. Posts
posts()

# 7. Status
status()
```

## Tools

- `start_discovery(niche, platform)` - Initialize
- `youtube(query)` - Scrape YouTube  
- `tiktok(hashtag)` - Scrape TikTok
- `instagram(username)` - Scrape Instagram
- `linkedin(profile_url)` - Scrape LinkedIn
- `select(index)` - Choose content
- `analyze()` - Extract insights
- `ideas()` - Generate concepts
- `posts()` - Create LinkedIn posts
- `status()` - Check progress

## Knowledge Base

- `knowledge_base/hooks.md` - 385+ LinkedIn hooks
- `knowledge_base/content_templates.md` - Content templates

Ready for viral LinkedIn content generation!