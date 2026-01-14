# MCP Toolkit - Quick Start Guide

## 🚀 TL;DR - What You Need to Know

### Do I Need VS Code?
**NO!** This is a standalone web application. Open it in **any browser**.

### What's Running?
```
Your Computer:
├── Python Application (ui_client.py, agent_service.py)
├── 3 Node.js MCP Servers (postgres, github, filesystem)
└── Web Server (Gradio) → http://localhost:7860
```

## 📋 Prerequisites

✅ **Python 3.11** - For running the application
✅ **Node.js** - For MCP servers (spawned automatically)
✅ **OpenAI API Key** - For AI responses (in .env)
✅ **PostgreSQL** - Your Adventureworks database
✅ **Web Browser** - Any browser (Chrome, Firefox, Safari)

❌ **NOT NEEDED**: VS Code, VS Code Copilot, any IDE

## ⚡ Quick Commands

```bash
# Start the application
./start.sh

# Stop the application  
./stop.sh

# View logs
tail -f /tmp/mcp_app.log
```

## 🌐 Access

Open in your browser: **http://localhost:7860**

## 🔧 How It Works (Simple)

```
1. You type a question in the web browser
   ↓
2. Python app sends it to OpenAI GPT-4
   ↓
3. GPT-4 decides which tool to use (database, GitHub, etc.)
   ↓
4. Python app calls the appropriate MCP server
   ↓
5. MCP server gets the data and returns it
   ↓
6. You see the answer in your browser
```

## 📝 Example Queries

Try asking:

**Database queries:**
- "Connect to postgres server"
- "List all tables in the database"
- "Show me data from the employees table"
- "How many employees are there?"

**GitHub queries:**
- "What are my GitHub repositories?"
- "Show me recent issues in my repos"

**File system queries:**
- "List all Python files in this directory"
- "Show me the contents of README.md"

## 🔐 Configuration Files

### `.env` - Your credentials
```bash
OPENAI_API_KEY=sk-proj-...      # Your OpenAI key
GITHUB_TOKEN=ghp_...            # Your GitHub token
DATABASE_URL=postgresql://...   # Your database URL
```

### `mcp_config.json` - MCP servers
```json
{
  "mcpServers": {
    "postgres": {...},    // Database server
    "github": {...},      // GitHub server
    "filesystem": {...}   // File system server
  }
}
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
./stop.sh  # Stop any running instances
./start.sh # Start fresh
```

**Server not responding:**
```bash
tail -20 /tmp/mcp_app.log  # Check for errors
```

**Database connection failed:**
- Check PostgreSQL is running on port 5431
- Verify DATABASE_URL in .env

**No response in chat:**
- Check OpenAI API key is valid
- Check logs for errors

## 📚 More Info

- Full architecture: See [ARCHITECTURE.md](ARCHITECTURE.md)
- MCP Protocol: https://modelcontextprotocol.io
- mcp-use library: https://github.com/sparfenyuk/mcp-use

## 🎯 Key Takeaways

1. **Standalone app** - No IDE required
2. **Browser-based** - Works on any device with a browser
3. **Your own LLM** - Uses your OpenAI API key
4. **Multiple data sources** - Database, GitHub, Files
5. **Easy to use** - Just type natural language questions

**You're running a full AI agent with database and API access, all in your browser! 🎉**
