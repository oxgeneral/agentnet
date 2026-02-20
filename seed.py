"""Seed the AgentNet registry with real agents from research."""

import registry

AGENTS = [
    # === Telegram Bots ===
    {"name": "Pixie Bot", "description": "AI image generation, QR codes, OCR, stickers, memes, compression",
     "capabilities": ["image_generation", "qr_codes", "ocr", "stickers", "memes", "image_compression"],
     "platform": "telegram", "endpoint": "https://t.me/toolbox_utils_bot"},

    {"name": "Astro Light", "description": "Daily horoscopes, tarot readings, compatibility, numerology",
     "capabilities": ["horoscope", "tarot", "compatibility", "numerology", "astrology"],
     "platform": "telegram", "endpoint": "https://t.me/astro_light_taro_bot"},

    {"name": "Midjourney Bot", "description": "AI art generation with Midjourney models",
     "capabilities": ["image_generation", "art", "ai_art", "creative"],
     "platform": "telegram", "endpoint": "https://t.me/MidjourneyOfficialBot"},

    {"name": "ChatGPT Telegram", "description": "ChatGPT conversational AI in Telegram",
     "capabilities": ["chat", "qa", "writing", "coding", "translation"],
     "platform": "telegram", "endpoint": "https://t.me/ChatGPT4o_Telegram_Bot"},

    {"name": "Remove.bg Bot", "description": "Remove image backgrounds automatically",
     "capabilities": ["background_removal", "image_editing", "photo_editing"],
     "platform": "telegram", "endpoint": "https://t.me/remove_bg_bot"},

    {"name": "Shazam Bot", "description": "Music recognition from audio messages",
     "capabilities": ["music_recognition", "audio", "shazam"],
     "platform": "telegram", "endpoint": "https://t.me/ShazamMusicRecognitionBot"},

    {"name": "SaveFrom Bot", "description": "Download videos from YouTube, TikTok, Instagram",
     "capabilities": ["video_download", "youtube", "tiktok", "instagram"],
     "platform": "telegram", "endpoint": "https://t.me/SaveFromBot"},

    {"name": "VoiceGPT", "description": "Voice-to-text and text-to-voice with AI",
     "capabilities": ["voice_recognition", "text_to_speech", "transcription"],
     "platform": "telegram", "endpoint": "https://t.me/VoiceGPTBot"},

    {"name": "PDF Bot", "description": "Convert, merge, split, compress PDF files",
     "capabilities": ["pdf", "document_conversion", "file_processing"],
     "platform": "telegram", "endpoint": "https://t.me/paborobot"},

    {"name": "Translate Bot", "description": "Translate text between 100+ languages",
     "capabilities": ["translation", "language", "multilingual"],
     "platform": "telegram", "endpoint": "https://t.me/YTranslateBot"},

    # === MCP Servers ===
    {"name": "Brave Search MCP", "description": "Web search and local search via Brave API",
     "capabilities": ["web_search", "local_search", "research"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/brave-search"},

    {"name": "Puppeteer MCP", "description": "Browser automation, screenshots, web scraping",
     "capabilities": ["browser_automation", "screenshots", "web_scraping"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/puppeteer"},

    {"name": "GitHub MCP", "description": "GitHub repository management, issues, PRs, code search",
     "capabilities": ["github", "code_management", "version_control", "issues"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/github"},

    {"name": "Filesystem MCP", "description": "Read, write, and manage files on disk",
     "capabilities": ["file_management", "read_files", "write_files"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/filesystem"},

    {"name": "SQLite MCP", "description": "Query and manage SQLite databases",
     "capabilities": ["database", "sql", "sqlite", "data_analysis"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/sqlite"},

    {"name": "Fetch MCP", "description": "Fetch web pages and convert to markdown",
     "capabilities": ["web_fetch", "html_to_markdown", "content_extraction"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/fetch"},

    {"name": "Memory MCP", "description": "Persistent memory storage using knowledge graphs",
     "capabilities": ["memory", "knowledge_graph", "persistent_storage"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/memory"},

    {"name": "Slack MCP", "description": "Send messages, manage channels, search Slack",
     "capabilities": ["slack", "messaging", "team_communication"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/slack"},

    {"name": "Google Maps MCP", "description": "Geocoding, directions, places search",
     "capabilities": ["maps", "geocoding", "directions", "places"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/google-maps"},

    {"name": "Sentry MCP", "description": "Error tracking and monitoring for applications",
     "capabilities": ["error_tracking", "monitoring", "debugging"],
     "platform": "mcp", "endpoint": "https://smithery.ai/server/@nicholasbutler/sentry"},

    # === GPT Store ===
    {"name": "DALL-E GPT", "description": "Image generation using DALL-E 3",
     "capabilities": ["image_generation", "art", "creative", "dalle"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-2fkFE8rbu-dall-e"},

    {"name": "Data Analyst GPT", "description": "Analyze data, create charts, insights from files",
     "capabilities": ["data_analysis", "charts", "visualization", "statistics"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-HMNcP6w7d-data-analyst"},

    {"name": "Scholar GPT", "description": "Academic research, paper analysis, citations",
     "capabilities": ["research", "academic", "papers", "citations"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-kZ0eYXlJe-scholar-gpt"},

    {"name": "Code Copilot GPT", "description": "Coding assistant, code review, debugging",
     "capabilities": ["coding", "code_review", "debugging", "programming"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-2DQzU5UZl-code-copilot"},

    {"name": "Logo Creator GPT", "description": "Design logos and brand identity",
     "capabilities": ["logo_design", "branding", "graphic_design"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-gFt1ghYJl-logo-creator"},

    {"name": "Canva GPT", "description": "Create presentations, social media posts, designs",
     "capabilities": ["design", "presentations", "social_media", "graphic_design"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-alKfVrz9K-canva"},

    {"name": "PDF AI GPT", "description": "Chat with PDF documents, extract and summarize",
     "capabilities": ["pdf", "document_analysis", "summarization"],
     "platform": "gpt", "endpoint": "https://chat.openai.com"},

    {"name": "Consensus GPT", "description": "Search academic papers and get evidence-based answers",
     "capabilities": ["research", "academic", "evidence", "science"],
     "platform": "gpt", "endpoint": "https://chat.openai.com/g/g-bo0FiWLY7-consensus"},

    # === Web/API Agents ===
    {"name": "AutoGPT", "description": "Autonomous AI agent that breaks down goals into tasks",
     "capabilities": ["autonomous", "task_planning", "web_browsing", "coding"],
     "platform": "web", "endpoint": "https://agpt.co"},

    {"name": "Devin", "description": "AI software engineer that can code, debug, and deploy",
     "capabilities": ["coding", "debugging", "deployment", "software_engineering"],
     "platform": "web", "endpoint": "https://devin.ai"},

    {"name": "Perplexity", "description": "AI-powered research and answer engine",
     "capabilities": ["research", "web_search", "qa", "summarization"],
     "platform": "web", "endpoint": "https://perplexity.ai"},

    {"name": "Cursor", "description": "AI-powered code editor with intelligent completions",
     "capabilities": ["coding", "code_completion", "refactoring", "ide"],
     "platform": "web", "endpoint": "https://cursor.com"},

    {"name": "v0 by Vercel", "description": "AI-powered UI generation from text prompts",
     "capabilities": ["ui_design", "frontend", "react", "web_development"],
     "platform": "web", "endpoint": "https://v0.dev"},

    {"name": "Replit Agent", "description": "AI that builds and deploys full applications",
     "capabilities": ["coding", "deployment", "full_stack", "app_building"],
     "platform": "web", "endpoint": "https://replit.com"},

    {"name": "Bolt.new", "description": "Full-stack AI app builder in the browser",
     "capabilities": ["coding", "full_stack", "web_development", "deployment"],
     "platform": "web", "endpoint": "https://bolt.new"},

    {"name": "Lovable", "description": "AI full-stack engineer for web apps",
     "capabilities": ["coding", "full_stack", "web_development", "ui_design"],
     "platform": "web", "endpoint": "https://lovable.dev"},

    # === Discord Bots ===
    {"name": "MEE6", "description": "Moderation, leveling, custom commands for Discord",
     "capabilities": ["moderation", "leveling", "custom_commands", "automation"],
     "platform": "discord", "endpoint": "https://mee6.xyz"},

    {"name": "Dyno Bot", "description": "Moderation, auto-roles, announcements for Discord",
     "capabilities": ["moderation", "auto_roles", "announcements"],
     "platform": "discord", "endpoint": "https://dyno.gg"},

    {"name": "Midjourney Discord", "description": "AI art generation via Discord commands",
     "capabilities": ["image_generation", "art", "ai_art"],
     "platform": "discord", "endpoint": "https://discord.gg/midjourney"},

    # === Specialized Agents ===
    {"name": "Salebot", "description": "CRM + bot builder for sales funnels in Telegram",
     "capabilities": ["crm", "sales", "funnels", "automation", "marketing"],
     "platform": "telegram", "endpoint": "https://salebot.pro"},

    {"name": "ManyChat", "description": "Marketing automation for Instagram, WhatsApp, Telegram",
     "capabilities": ["marketing", "automation", "chat_flows", "broadcasts"],
     "platform": "web", "endpoint": "https://manychat.com"},

    {"name": "n8n", "description": "Workflow automation connecting 400+ apps",
     "capabilities": ["automation", "workflows", "integrations", "api_orchestration"],
     "platform": "web", "endpoint": "https://n8n.io"},

    {"name": "Relevance AI", "description": "Build and deploy AI agents for business tasks",
     "capabilities": ["agent_builder", "business_automation", "no_code"],
     "platform": "web", "endpoint": "https://relevanceai.com"},

    {"name": "Lindy AI", "description": "Personal AI assistant for business workflows",
     "capabilities": ["personal_assistant", "email", "scheduling", "automation"],
     "platform": "web", "endpoint": "https://lindy.ai"},

    {"name": "Adsgram", "description": "Ad network for Telegram Mini Apps and bots",
     "capabilities": ["advertising", "monetization", "telegram_ads"],
     "platform": "telegram", "endpoint": "https://adsgram.ai"},

    {"name": "Graspil", "description": "Analytics and admin panel for Telegram bots",
     "capabilities": ["analytics", "admin_panel", "bot_management"],
     "platform": "telegram", "endpoint": "https://graspil.com"},

    {"name": "InviteMember", "description": "Subscription management for paid Telegram channels",
     "capabilities": ["subscriptions", "payments", "membership"],
     "platform": "telegram", "endpoint": "https://invitemember.com"},
]


def seed():
    count = 0
    for agent in AGENTS:
        result = registry.register_agent(**agent)
        if "id" in result:
            count += 1
            print(f"  + {agent['name']} ({agent['platform']})")
        else:
            print(f"  ~ {agent['name']}: {result.get('error', 'unknown')}")
    print(f"\nSeeded {count}/{len(AGENTS)} agents")
    stats = registry.get_network_stats()
    print(f"Network: {stats['total_agents']} agents")


if __name__ == "__main__":
    seed()
