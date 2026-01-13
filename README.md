# MCP Toolkit

A Python-based AI Agent toolkit for interacting with PostgreSQL databases and GitHub using the Model Context Protocol (MCP).

## Features

- 🤖 **AI Agent**: Natural language interface powered by multiple LLMs
  - **VS Code Copilot / GitHub Models** (recommended)
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude 3.5)
  - Groq (ultra-fast inference)
- 🗄️ **PostgreSQL Integration**: Query and manage databases conversationally
- 🐙 **GitHub Integration**: Manage repositories, issues, and PRs
- 🌐 **Web UI**: Beautiful Gradio interface for easy interaction
- 💬 **Conversation Memory**: Maintains context across queries
- ⚡ **Streaming Responses**: Real-time agent output
- 🔧 **Extensible**: Easy to add new MCP servers
- 💰 **Cost Effective**: Use GitHub Models free tier or your Copilot subscription

## Architecture

```
┌─────────────────────┐
│   Gradio Web UI     │ ← User Interface
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AI Agent          │ ← Natural Language Processing
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   MCP Client        │ ← Protocol Handler
└──────────┬──────────┘
           │
           ├──────────────┬──────────────┐
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Postgres  │   │ GitHub   │   │Filesystem│
    │MCP Server│   │MCP Server│   │MCP Server│
    └──────────┘   └──────────┘   └──────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for MCP servers)
- PostgreSQL database (optional for testing)
- GitHub Personal Access Token

### Installation

```bash
# Clone the repository
git clone https://github.com/majidraza1228/mcp-toolkit.git
cd mcp-toolkit

# Install Python dependencies
pip install -r requirements.txt

# Verify Node.js is installed
node --version  # Should show v18+
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
nano .env  # or use your preferred editor
```

**Required environment variables:**
```bash
# Choose LLM Provider (recommended: github for VS Code Copilot users)
LLM_PROVIDER=github

# Option 1: VS Code Copilot / GitHub Models (FREE/INCLUDED)
GITHUB_TOKEN=ghp_...
GITHUB_MODELS_API_KEY=${GITHUB_TOKEN}
LLM_MODEL=gpt-4o

# Option 2: Standard OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...

# Option 3: Anthropic Claude
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...

# PostgreSQL Connection
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

**📖 New to GitHub Models?** See [VSCODE_COPILOT_SETUP.md](VSCODE_COPILOT_SETUP.md) for detailed setup instructions.

### Run

```bash
# Launch the application
python run.py
```

The web UI will open at [http://localhost:7860](http://localhost:7860)

## Usage Examples

### Example 1: Database Queries
```
User: "List all tables in my database"
Agent: *Queries PostgreSQL and returns table list*
```

### Example 2: GitHub Operations
```
User: "Show me my repositories with the most stars"
Agent: *Fetches repos from GitHub and sorts by stars*
```

### Example 3: Cross-Server Workflows
```
User: "Find all developers in my database and check their GitHub activity"
Agent: *Queries database, then checks each developer's GitHub profile*
```

## Project Structure

```
mcp-toolkit/
├── README.md                    # This file
├── QUICKSTART.md               # 5-minute setup guide
├── ARCHITECTURE.md             # Detailed architecture
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── mcp_config.json            # MCP servers configuration
│
├── run.py                     # Main launcher
├── agent_service.py           # AI Agent implementation
├── ui_client.py              # Gradio web interface
│
├── utils/                     # Utility modules
│   ├── mcp_manager.py        # MCP client wrapper
│   └── prompts.py            # System prompts
│
└── examples/                  # Usage examples
    ├── basic_query.py
    ├── streaming_example.py
    ├── multi_step_task.py
    └── direct_tool_call.py
```

## Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [VS Code Copilot Setup](VSCODE_COPILOT_SETUP.md) - Use GitHub Models / Copilot as your LLM
- [Architecture Guide](ARCHITECTURE.md) - Deep dive into the system
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical overview

## Available MCP Servers

The toolkit connects to these MCP servers:

1. **PostgreSQL** - Database operations
   - Execute SQL queries
   - Inspect schema
   - Manage data

2. **GitHub** - Repository management
   - List repositories
   - Create issues and PRs
   - Search code

3. **Filesystem** (optional) - File operations
   - Read/write files
   - Navigate directories
   - Search files

## Customization

### Add New MCP Server

Edit `mcp_config.json`:
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_TOKEN": "${SLACK_TOKEN}"
      }
    }
  }
}
```

### Change LLM Provider

Simply change `LLM_PROVIDER` in `.env`:
- `github` - VS Code Copilot / GitHub Models (recommended)
- `openai` - Standard OpenAI API
- `anthropic` - Anthropic Claude
- `groq` - Ultra-fast inference

No code changes needed! See [VSCODE_COPILOT_SETUP.md](VSCODE_COPILOT_SETUP.md) for details.

### Customize Agent Behavior

Edit `utils/prompts.py` to change how the agent behaves:
- Add safety rules
- Change tone/style
- Add domain-specific instructions

## Running Examples

```bash
# Basic query example
python examples/basic_query.py

# Streaming responses
python examples/streaming_example.py

# Multi-step workflow
python examples/multi_step_task.py

# Direct tool calls (no LLM)
python examples/direct_tool_call.py
```

## Troubleshooting

### MCP Server Connection Issues

Test servers manually:
```bash
# Test Postgres server
npx @modelcontextprotocol/server-postgres postgresql://localhost/mydb

# Test GitHub server
GITHUB_TOKEN=your_token npx @modelcontextprotocol/server-github
```

### Database Connection Errors

```bash
# Test database connection
psql $DATABASE_URL

# Check if PostgreSQL is running
pg_isready
```

### Missing API Keys

Ensure your `.env` file has at least one LLM provider configured:
- `GITHUB_MODELS_API_KEY` or `GITHUB_TOKEN` (for GitHub Models)
- `OPENAI_API_KEY` (for OpenAI)
- `ANTHROPIC_API_KEY` (for Anthropic)

See [VSCODE_COPILOT_SETUP.md](VSCODE_COPILOT_SETUP.md) for setup instructions.

## Dependencies

### Python Packages
- `mcp-use` - MCP client and agent framework
- `gradio` - Web UI framework
- `langchain` - LLM orchestration
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable management

### Node.js Packages (auto-installed)
- `@modelcontextprotocol/server-postgres` - PostgreSQL MCP server
- `@modelcontextprotocol/server-github` - GitHub MCP server
- `@modelcontextprotocol/server-filesystem` - Filesystem MCP server

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with:
- [mcp-use](https://github.com/modelcontextprotocol/mcp-use) - MCP framework
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification
- [Gradio](https://gradio.app) - Web UI framework
- [LangChain](https://python.langchain.com) - LLM framework

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/majidraza1228/mcp-toolkit/issues)
- Check the documentation files in this repository

---

**Ready to get started?**

```bash
python run.py
```

Happy building! 🚀
