# LinkedIn Viral Content Generator MCP Server

A FastMCP server that integrates with Apify actors to scrape social media content and generate viral LinkedIn posts using hook templates and content patterns.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Apify API token (get one at [apify.com](https://apify.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ankaravanas/viral-linkedin-content-generator.git
   cd viral-linkedin-content-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your APIFY_TOKEN
   ```

### 🔌 MCP Client Connection

**IMPORTANT**: This is an MCP (Model Context Protocol) server that uses stdio transport.

#### For Claude Desktop

Add to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "viral-linkedin-content-generator": {
      "command": "python3",
      "args": ["/absolute/path/to/viral-linkedin-content-generator/server.py"],
      "env": {
        "APIFY_TOKEN": "your_apify_token_here"
      }
    }
  }
}
```

#### For Other MCP Clients

Use these connection parameters:
- **Command**: `python3`
- **Args**: `["/path/to/server.py"]`
- **Environment**: `{"APIFY_TOKEN": "your_token"}`
- **Transport**: stdio (default)

### 🧪 Test the Server

#### Local Testing (stdio transport):
```bash
# Test server import and basic functionality
python3 -c "import server; print('✅ Server loads successfully')"

# Test knowledge base loading
python3 -c "import server; kb = server.load_knowledge_base(); print(f'✅ Knowledge base loaded: {len(kb[\"hooks\"])} chars hooks, {len(kb[\"content_templates\"])} chars templates')"

# Run server locally
python3 server.py
```

#### HTTP Testing (SSE transport):
```bash
# Test with HTTP/SSE transport
PORT=8000 python3 server.py
# Server will be available at http://localhost:8000/sse

# Test with FastMCP Inspector
npx @mcpjam/inspector@latest
# Connect to http://localhost:8000/sse in the Inspector UI
```

## ✨ Features

- **Multi-platform scraping**: YouTube, TikTok, Instagram, LinkedIn via Apify actors
- **385+ Hook Templates**: Comprehensive LinkedIn hook library across 14 categories
- **Content analysis**: Extract key metrics, insights, and engagement patterns
- **Intelligent hook matching**: AI-powered selection from knowledge base
- **Automated post generation**: Create viral LinkedIn content using proven templates

## 🔄 Workflow

The server provides a complete 8-step workflow:

1. **Topic Discovery**: `start_content_discovery(niche, platform)`
2. **Content Scraping**: Platform-specific scraping tools
3. **Content Selection**: `select_content(index)`
4. **Engagement Analysis**: `analyze_comments()`
5. **Content Analysis**: `analyze_content_transcript()`
6. **Hook Selection**: `select_hooks([indices])`
7. **Idea Generation**: `generate_content_ideas()`
8. **Post Creation**: `generate_linkedin_posts()`

## 🛠 Available MCP Tools

### Content Discovery
- `start_content_discovery(niche, platform)` - Initialize workflow
- `get_workflow_status()` - Track progress

### Platform Scraping
- `scrape_youtube_videos(search_query, max_results=5)` - YouTube content discovery
- `scrape_tiktok_videos(hashtag, results_per_page=15)` - TikTok content discovery  
- `scrape_instagram_posts(username, results_limit=12)` - Instagram content discovery
- `scrape_linkedin_posts(profile_url)` - LinkedIn content discovery

### Content Analysis
- `select_content(index)` - Choose content for analysis
- `analyze_comments()` - Extract engagement insights
- `analyze_content_transcript()` - Content analysis

### Content Generation
- `select_hooks(hook_indices)` - Hook selection from knowledge base
- `generate_content_ideas()` - Create content concepts
- `generate_linkedin_posts(selected_idea_index=1)` - Generate final LinkedIn posts

## 📚 Knowledge Base

The server includes comprehensive templates:

- **`knowledge_base/hooks.md`**: 385+ LinkedIn hook templates across 14 categories
  - Carousel, Story, Viral, Creative, Image, Funny
  - Success, Mistake, Polarising, Question, Pain Point
  - Desire, Fear-based, Shocking, Conflict, and more

- **`knowledge_base/content_templates.md`**: Detailed post templates with proven copywriting formulas
  - AIDA framework, pain point addressing, engagement strategies

## 🎯 Example Usage

Once connected via MCP client:

```
1. start_content_discovery("AI automation tools", "youtube")
2. scrape_youtube_videos("AI automation tools")
3. select_content(1)  # Choose first video
4. analyze_comments()
5. analyze_content_transcript()
6. select_hooks([1, 2, 3])  # Choose hooks
7. generate_content_ideas()
8. generate_linkedin_posts()
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're using Python 3.8+ and have installed dependencies
2. **APIFY_TOKEN Error**: Ensure your Apify token is set in the environment
3. **MCP Connection**: Verify you're using the correct absolute path in MCP client config

### Debug Commands

```bash
# Test FastMCP import
python3 -c "from fastmcp import FastMCP; print('✅ FastMCP working')"

# Test server import
python3 -c "import server; print('✅ Server working')"

# Check knowledge base
python3 -c "import server; kb = server.load_knowledge_base(); print('Hooks:', len(kb['hooks']), 'Templates:', len(kb['content_templates']))"
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.