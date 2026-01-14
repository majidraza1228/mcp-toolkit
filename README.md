# 🤖 MCP Toolkit - AI Agent with Database & API Access

A standalone Python application that uses the Model Context Protocol (MCP) to connect AI agents to databases, APIs, and file systems through a web-based chat interface.

## 🌟 What Is This?

This is a **browser-based AI chat application** that can:
- 💾 Query your PostgreSQL database with natural language
- 🐙 Interact with GitHub repositories
- 📁 Access and search local files
- 🤖 Use AI (GPT-4) to understand and respond to your questions

**No VS Code required** - runs completely standalone in your web browser!

## 🚀 Quick Start

```bash
# Start the application
./start.sh

# Open in your browser
# http://localhost:7860

# Stop when done
./stop.sh
```

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand how it works
- **[mcp_config.json](mcp_config.json)** - Configure MCP servers
- **[.env](.env)** - Set your API keys and credentials

## ✨ Features

### 🗣️ Natural Language Interface
Ask questions in plain English:
```
"Show me all tables in the database"
"How many employees are in the company?"
"What are my recent GitHub repositories?"
"List all Python files in this directory"
```

### 🔌 Multiple Data Sources via MCP
- **PostgreSQL** - Query your Adventureworks database
- **GitHub** - Access repos, issues, code
- **Filesystem** - Read and search local files

### 🧠 AI-Powered
- Uses OpenAI GPT-4 (your API key)
- Automatically chooses the right tool
- Provides natural language responses

### 🌐 Web-Based UI
- Clean chat interface (Gradio)
- Works in any browser
- No installation required for end users

## 🏗️ Architecture

```
Browser → Python App → AI Agent → MCP Servers → Data Sources
                                   ├─ PostgreSQL
                                   ├─ GitHub API
                                   └─ Filesystem
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed explanation.

## 📋 Requirements

- **Python 3.11+** - Main application
- **Node.js** - For MCP servers
- **PostgreSQL** - Your database
- **OpenAI API Key** - For AI responses
- **GitHub Token** - For GitHub access (optional)

## 🔧 Installation

1. **Clone or download this repository**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Edit `.env` file:
   ```bash
   OPENAI_API_KEY=your-key-here
   GITHUB_TOKEN=your-token-here
   DATABASE_URL=postgresql://user:pass@localhost:5431/db
   ```

4. **Start the application**
   ```bash
   ./start.sh
   ```

5. **Open in browser**
   Navigate to: http://localhost:7860

## 💬 Example Conversations

### Database Queries
```
You: Connect to postgres server
Agent: Connected! 6 tools are now available.

You: List all tables
Agent: Here are the tables:
      1. employees
      2. product_reviews

You: Show me data from employees table
Agent: [Displays employee data]
```

### GitHub Queries
```
You: What are my GitHub repositories?
Agent: You have 15 repositories:
      1. mcp-toolkit - AI agent application
      2. python-scripts - Utility scripts
      ...
```

### File System
```
You: List all Python files
Agent: Found 5 Python files:
      - run.py
      - ui_client.py
      - agent_service.py
      ...
```

## 🔐 Security Notes

- Keep your `.env` file private (contains API keys)
- Don't commit `.env` to version control
- MCP servers run as local processes with your permissions
- Database access uses your credentials

## 🆚 vs VS Code Copilot

| Feature | MCP Toolkit | VS Code Copilot |
|---------|-------------|-----------------|
| Requires VS Code | ❌ No | ✅ Yes |
| Interface | Web Browser | IDE |
| Database Access | ✅ Yes | Limited |
| Custom MCP Servers | ✅ Yes | Limited |
| Deployment | Server | Desktop |
| Your API Key | ✅ Yes | No |

## 🐛 Troubleshooting

**Application won't start:**
- Check Python version: `/usr/local/bin/python3.11 --version`
- Check Node.js: `node --version`
- View logs: `tail -f /tmp/mcp_app.log`

**Database connection fails:**
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Test connection: `psql $DATABASE_URL`

**No AI responses:**
- Verify `OPENAI_API_KEY` in `.env`
- Check OpenAI account has credits
- Check logs for API errors

**Port 7860 in use:**
```bash
./stop.sh  # Kill any existing instances
./start.sh # Start fresh
```

## 📚 Learn More

- **MCP Protocol**: https://modelcontextprotocol.io
- **mcp-use Library**: https://github.com/sparfenyuk/mcp-use
- **Gradio**: https://gradio.app
- **LangChain**: https://langchain.com

## 🤝 Contributing

Feel free to:
- Add new MCP servers
- Improve the UI
- Add new features
- Report bugs

## 📝 License

[Your license here]

## 🎉 Credits

Built with:
- [mcp-use](https://github.com/sparfenyuk/mcp-use) - MCP client library
- [Gradio](https://gradio.app) - Web UI framework
- [LangChain](https://langchain.com) - AI agent framework
- [Model Context Protocol](https://modelcontextprotocol.io) - Standard protocol

---

**Happy Chatting with Your Data! 🚀**
