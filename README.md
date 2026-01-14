# 🤖 MCP Toolkit - AI Agent with Database & API Access

A standalone Python application that uses the Model Context Protocol (MCP) to connect AI agents to databases, APIs, and file systems through a web-based chat interface.

![AI Agent Interface](docs/screenshots/ai-agent-interface.png)
*Professional dark theme with self-learning capabilities, MCP server selector, and real-time feedback*

## 🌟 What Is This?

This is a **browser-based AI chat application** that can:
- 💾 Query your PostgreSQL database with natural language
- 🐙 Interact with GitHub repositories
- 📁 Access and search local files
- 🤖 Use AI (GPT-4) to understand and respond to your questions
- 🧠 Learn from your feedback and get faster over time

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

### Core Documentation
- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Architecture Overview](docs/ARCHITECTURE.md)** - Understand how it works
- **[Learning System](docs/LEARNING_SYSTEM.md)** - Self-learning capabilities explained

### Advanced Topics
- **[AI Agent Explained](docs/AI_AGENT_EXPLAINED.md)** - What makes this a true AI agent
- **[Self-Learning Guide](docs/SELF_LEARNING_GUIDE.md)** - Advanced learning strategies
- **[Getting Started](docs/GETTING_STARTED.md)** - Detailed setup instructions
- **[VS Code Copilot Setup](docs/VSCODE_COPILOT_SETUP.md)** - Optional VS Code integration
- **[Python Version Guide](docs/PYTHON_VERSION_GUIDE.md)** - Python version management

### Configuration
- **[mcp_config.json](mcp_config.json)** - Configure MCP servers
- **[.env](.env)** - Set your API keys and credentials

### Additional Resources
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[Screenshots Guide](docs/screenshots/HOW_TO_ADD_SCREENSHOT.md)** - How to add interface screenshots

## ✨ Features

### 🗣️ Natural Language Interface
Ask questions in plain English:
```
"Show me all tables in the database"
"How many employees are in the company?"
"What are my recent GitHub repositories?"
"List all Python files in this directory"
```

### 🧠 Self-Learning System (NEW!)
- **Query Caching**: 20-30x faster responses for repeated queries
- **User Feedback**: 👍/👎 buttons to rate responses
- **Smart Retrieval**: Only serves high-quality cached responses
- **Learning Dashboard**: Track cache hits and feedback metrics
- **Persistent Memory**: Learns across sessions and improves over time

### 🎨 Professional Interface
- **Dark Theme**: Modern, eye-friendly design
- **MCP Server Selector**: Choose which server to use (postgres/github/filesystem/all)
- **Real-time Statistics**: Monitor learning progress
- **Feedback Buttons**: Rate responses to improve future results

### 🔌 Multiple Data Sources via MCP
- **PostgreSQL** - Query your database with natural language
- **GitHub** - Access repos, issues, pull requests, and code
- **Filesystem** - Read and search local files
- **Extensible** - Add your own MCP servers

### 🤖 AI-Powered
- Uses OpenAI GPT-4 (your API key)
- Automatically chooses the right tool for each task
- Provides natural language responses
- Learns from user feedback

### 🌐 Web-Based UI
- Clean chat interface powered by Gradio
- Works in any modern browser
- No installation required for end users
- Mobile-friendly responsive design

## 🏗️ Architecture

```
Browser → Python App → AI Agent → MCP Servers → Data Sources
                                   ├─ PostgreSQL
                                   ├─ GitHub API
                                   └─ Filesystem
```

The application uses a ReAct (Reasoning + Acting) agent pattern that:
1. Receives your natural language query
2. Reasons about which tools to use
3. Executes actions through MCP servers
4. Returns results in natural language
5. Caches responses for future speed improvements

See [Architecture Overview](docs/ARCHITECTURE.md) for detailed explanation.

## 📋 Requirements

- **Python 3.11+** - Main application (required for mcp-use library)
- **Node.js** - For MCP servers
- **PostgreSQL** - Your database (optional, for database queries)
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
You: List all employees in the database
Agent: Here are all the employees:

1. Employee ID: 1
   First Name: John
   Last Name: Doe
   Department: Marketing
   Salary: 55000.00

2. Employee ID: 2
   First Name: Jane
   ...

👍 [Click to rate this response]
```

### GitHub Queries
```
You: Show my public repositories
Agent: You have 12 public repositories:

1. mcp-toolkit - AI agent application
2. python-scripts - Utility scripts
...

👍 [Response cached for faster future retrieval]
```

### File System
```
You: List all Python files
Agent: Found 5 Python files:
      - run.py
      - ui_client.py
      - agent_service.py
      - utils/mcp_manager.py
      - utils/simple_memory.py
```

## 🧠 Self-Learning in Action

The agent learns from your interactions:

1. **First Query**: "List all users" → 2.5 seconds (full processing)
2. **Click 👍**: Marks response as good quality
3. **Second Query**: "show all users" → 0.1 seconds (cached) ⚡
4. **Result**: 25x faster!

See [Learning System](docs/LEARNING_SYSTEM.md) for complete details.

## 🔐 Security Notes

- Keep your `.env` file private (contains API keys)
- Don't commit `.env` to version control (it's in `.gitignore`)
- MCP servers run as local processes with your permissions
- Database access uses your credentials
- All data stays on your machine

## 🆚 vs VS Code Copilot

| Feature | MCP Toolkit | VS Code Copilot |
|---------|-------------|-----------------|
| Requires VS Code | ❌ No | ✅ Yes |
| Interface | Web Browser | IDE |
| Database Access | ✅ Full SQL queries | Limited |
| GitHub Access | ✅ Full API access | Limited |
| Custom MCP Servers | ✅ Yes | Limited |
| Self-Learning | ✅ Yes | No |
| Deployment | Anywhere | Desktop only |
| Your API Key | ✅ Yes | No |
| Open Source | ✅ Yes | No |

## 🐛 Troubleshooting

### Application won't start
- Check Python version: `/usr/local/bin/python3.11 --version`
- Check Node.js: `node --version`
- View logs: `tail -f /tmp/mcp_app.log`
- Stop existing instances: `./stop.sh`

### Database connection fails
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Test connection: `psql $DATABASE_URL`

### No AI responses
- Verify `OPENAI_API_KEY` in `.env`
- Check OpenAI account has credits
- Check logs for API errors

### Port 7860 in use
```bash
./stop.sh  # Kill any existing instances
./start.sh # Start fresh
```

### Recursion limit errors
- Agent increased to 30 steps (from default 5)
- Break complex queries into smaller parts
- Check that required MCP servers are connected

See [Troubleshooting Guide](docs/ARCHITECTURE.md#troubleshooting) for more help.

## 📊 Performance

- **Query caching**: 20-30x faster for repeated queries
- **Cache hit rate**: Improves to 50-80% over time
- **Response time**:
  - Cached: 0.1 seconds
  - Fresh: 2-3 seconds
  - Average: 0.7-1.5 seconds (after learning)

## 📚 Learn More

### About This Project
- [Architecture Overview](docs/ARCHITECTURE.md)
- [AI Agent Capabilities](docs/AI_AGENT_EXPLAINED.md)
- [Self-Learning System](docs/LEARNING_SYSTEM.md)

### External Resources
- **MCP Protocol**: https://modelcontextprotocol.io
- **mcp-use Library**: https://github.com/sparfenyuk/mcp-use
- **Gradio**: https://gradio.app
- **LangChain**: https://langchain.com

## 🤝 Contributing

We welcome contributions! Feel free to:
- Add new MCP servers
- Improve the UI and user experience
- Enhance learning capabilities
- Add new features
- Fix bugs
- Improve documentation

See [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md) for technical details.

## 📝 License

[Your license here]

## 🎉 Credits

Built with:
- [mcp-use](https://github.com/sparfenyuk/mcp-use) - MCP client library
- [Gradio](https://gradio.app) - Web UI framework
- [LangChain](https://langchain.com) - AI agent framework
- [Model Context Protocol](https://modelcontextprotocol.io) - Standard protocol
- [OpenAI GPT-4](https://openai.com) - Language model

---

**Happy Chatting with Your Data! 🚀**

*The agent learns from every interaction, becoming faster and smarter with each use.*
