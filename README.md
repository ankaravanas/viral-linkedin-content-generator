# LinkedIn Viral Content Generator MCP Server

Transform social media insights into viral LinkedIn posts using AI-powered content analysis.

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/ankaravanas/viral-linkedin-content-generator.git
cd viral-linkedin-content-generator
pip install -r requirements.txt
```

### Environment Setup

```bash
cp .env.example .env
# Edit .env and add your APIFY_TOKEN
```

### Run the Server

```bash
python linkedin_mcp.py
```

## 🔌 MCP Client Connection

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "linkedin-content-generator": {
      "command": "python3",
      "args": ["/absolute/path/to/viral-linkedin-content-generator/linkedin_mcp.py"],
      "env": {
        "APIFY_TOKEN": "your_apify_token_here"
      }
    }
  }
}
```

## 🛠 Available Tools

### Content Discovery
- `start_content_discovery(niche, platform)` - Initialize workflow
- `scrape_youtube(search_query, max_results=5)` - YouTube content research
- `scrape_tiktok(hashtag, max_results=10)` - TikTok content research
- `scrape_instagram(username, max_posts=12)` - Instagram content research
- `scrape_linkedin(profile_url)` - LinkedIn content research

### Content Analysis
- `select_content(index)` - Choose content for analysis
- `analyze_selected_content()` - Extract insights and metrics
- `analyze_engagement()` - Analyze comments and engagement

### LinkedIn Post Generation
- `generate_content_ideas()` - Create content concepts
- `create_linkedin_posts(idea_index=1)` - Generate final LinkedIn posts
- `get_workflow_status()` - Track workflow progress

## 🔄 Complete Workflow

```python
# 1. Start discovery
start_content_discovery("AI automation", "youtube")

# 2. Find content
scrape_youtube("AI automation tools")

# 3. Select content
select_content(1)  # Choose first video

# 4. Analyze content
analyze_selected_content()

# 5. Analyze engagement (optional)
analyze_engagement()

# 6. Generate ideas
generate_content_ideas()

# 7. Create LinkedIn posts
create_linkedin_posts()

# 8. Check status anytime
get_workflow_status()
```

## 📚 Knowledge Base

The server includes comprehensive templates:

- **`knowledge_base/hooks.md`**: 385+ LinkedIn hook templates across 14 categories
- **`knowledge_base/content_templates.md`**: Detailed post templates with copywriting formulas

## ✨ Features

- **Multi-platform scraping** via Apify actors (YouTube, TikTok, Instagram, LinkedIn)
- **Intelligent content analysis** with metrics extraction
- **Hook template matching** from comprehensive knowledge base
- **Automated LinkedIn post generation** with proven formats
- **Complete workflow tracking** from discovery to publication

## 🧪 Testing

Test with the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
# Connect to your local server via stdio transport
```

## 🎯 Example Output

The server generates 3 LinkedIn posts in different formats:
1. **Problem-Solution** format with data insights
2. **Story-driven** format with personal experience
3. **Contrarian** format with bold opinions

All posts are optimized for LinkedIn engagement and include calls-to-action.

## 📄 License

MIT License