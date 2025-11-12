# LinkedIn Viral Content Generator MCP Server

A FastMCP server that integrates with Apify actors to scrape social media content and generate viral LinkedIn posts using hook templates and content patterns.

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env and add your APIFY_TOKEN
   ```

3. **Run the Server**
   ```bash
   python server.py
   ```

### 🔌 MCP Client Connection

**IMPORTANT**: This is an MCP (Model Context Protocol) server, NOT an HTTP API server.

#### For Claude Desktop / MCP Clients:

Add to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "viral-linkedin-content-generator": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "APIFY_TOKEN": "your_apify_token_here"
      }
    }
  }
}
```

#### For Railway Deployment:

The server is deployed as a worker process on Railway. To connect:

1. **Set Environment Variables** in Railway:
   - `APIFY_TOKEN`: Your Apify API token

2. **Connection**: MCP servers use stdio transport - they cannot be accessed via HTTP URLs like `https://domain.com/mcp`

## ✨ Features

- **Multi-platform scraping**: YouTube, TikTok, Instagram, LinkedIn via Apify actors
- **385+ Hook Templates**: Comprehensive LinkedIn hook library across 14 categories
- **Content analysis**: Extract key metrics, insights, and engagement patterns
- **Intelligent hook matching**: AI-powered selection from knowledge base
- **Automated post generation**: Create viral LinkedIn content using proven templates

## 🔄 Workflow

1. **Topic Discovery**: `start_content_discovery(niche, platform)`
2. **Content Scraping**: Platform-specific scraping tools
3. **Content Selection**: `select_content(index)`
4. **Engagement Analysis**: `analyze_comments()`
5. **Content Analysis**: `analyze_content_transcript()`
6. **Hook Selection**: `select_hooks([indices])`
7. **Idea Generation**: `generate_content_ideas()`
8. **Post Creation**: `generate_linkedin_posts()`

## 📚 Knowledge Base

- **`hooks.md`**: 385+ LinkedIn hook templates across 14 categories
- **`content_templates.md`**: Detailed post templates with proven copywriting formulas

## 🛠 Available Tools

- `start_content_discovery()` - Initialize workflow
- `scrape_youtube_videos()` - YouTube content discovery
- `scrape_tiktok_videos()` - TikTok content discovery  
- `scrape_instagram_posts()` - Instagram content discovery
- `scrape_linkedin_posts()` - LinkedIn content discovery
- `select_content()` - Choose content for analysis
- `analyze_comments()` - Extract engagement insights
- `analyze_content_transcript()` - Content analysis
- `select_hooks()` - Hook selection from knowledge base
- `generate_content_ideas()` - Create content concepts
- `generate_linkedin_posts()` - Generate final LinkedIn posts
- `get_workflow_status()` - Track progress

## 🚂 Railway Deployment

This server is configured for Railway deployment as a worker process. It uses stdio transport for MCP communication, not HTTP endpoints.
