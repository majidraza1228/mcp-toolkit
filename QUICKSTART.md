# Quick Start Guide

Get up and running with the Python Full-Stack MCP Application in 5 minutes!

## Prerequisites

- **Python 3.11+** installed
- **Node.js 18+** installed (for MCP servers)
- **PostgreSQL** database running (optional for testing)
- **GitHub Personal Access Token** (create at https://github.com/settings/tokens)

## 1. Install Dependencies

```bash
cd examples/python-full-stack

# Install Python packages
pip install -r requirements.txt

# Verify Node.js is installed
node --version  # Should show v18+ or higher
```

## 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials
nano .env  # or use your favorite editor
```

**Required variables in `.env`:**
```bash
# At least one LLM API key
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# GitHub token
GITHUB_TOKEN=ghp_...

# PostgreSQL connection (use test DB if you want)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

## 3. Run the Application

```bash
# Run everything with one command
python run.py
```

This will:
1. Check your environment setup
2. Test MCP server connections
3. Launch the web UI at http://localhost:7860

## 4. Try It Out!

Once the UI loads:

1. **Test Database Query:**
   ```
   List all tables in my database
   ```

2. **Test GitHub Query:**
   ```
   Show me my GitHub repositories
   ```

3. **Test Cross-Server Task:**
   ```
   Find developers in my database and check their GitHub activity
   ```

## Alternative: Run Components Separately

### Terminal 1 - Test Agent (No UI)
```bash
python agent_service.py
```

### Terminal 2 - Launch UI
```bash
python ui_client.py
```

### Terminal 3 - Run Examples
```bash
# Basic query
python examples/basic_query.py

# Streaming responses
python examples/streaming_example.py

# Multi-step workflow
python examples/multi_step_task.py

# Direct tool calls (no LLM)
python examples/direct_tool_call.py
```

## Troubleshooting

### MCP Server Not Connecting

Test servers manually:

```bash
# Test Postgres server
npx @modelcontextprotocol/server-postgres postgresql://localhost/mydb

# Test GitHub server
GITHUB_TOKEN=your_token npx @modelcontextprotocol/server-github
```

### Database Connection Error

```bash
# Test your database connection
psql $DATABASE_URL

# Or check if PostgreSQL is running
pg_isready
```

### Missing API Keys

Make sure your `.env` file has at least one of:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GROQ_API_KEY`

## What's Next?

- **Customize MCP Servers**: Edit [mcp_config.json](mcp_config.json) to add/remove servers
- **Customize System Prompt**: Edit [utils/prompts.py](utils/prompts.py)
- **Add New Tools**: Connect more MCP servers
- **Deploy**: Use Docker or cloud platforms

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review example code in the `examples/` directory
- Open an issue in the main mcp-use repository

---

**That's it! You're ready to build AI-powered applications with MCP!** 🚀
