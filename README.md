# LinkedIn Viral Content Generator MCP Server

A minimal FastMCP server that integrates with Apify actors to scrape social media content and generate viral LinkedIn posts using hook templates and content patterns.

## Setup

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

## Features

- **Multi-platform scraping**: YouTube, TikTok, Instagram, LinkedIn via Apify actors
- **Content analysis**: Extract key metrics, insights, and engagement patterns
- **Hook matching**: Intelligent selection from knowledge base templates
- **Post generation**: Automated LinkedIn content creation using proven templates

## Workflow

1. Topic discovery and niche selection
2. Platform selection (YouTube/TikTok/Instagram/LinkedIn)
3. Content discovery and video selection
4. Comment/engagement analysis
5. Transcript/content analysis
6. Hook framework selection from knowledge base
7. Content formulation and approval
8. LinkedIn post generation using templates

## Knowledge Base

Update the files in `knowledge_base/` with your hook templates and content patterns:
- `hooks.md`: LinkedIn hook examples
- `content_templates.md`: Post template structures

## Deployment

Ready for Railway deployment with minimal configuration required.
