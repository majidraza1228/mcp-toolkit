# Getting Started with MCP Toolkit

Quick guide to get your AI agent running with VS Code Copilot or OpenAI.

## 🎯 What You'll Build

An AI agent that can:
- Query your PostgreSQL database in natural language
- Manage GitHub repositories
- Execute complex multi-step workflows
- All through a beautiful web interface

## 📋 Prerequisites Checklist

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] GitHub account with Personal Access Token
- [ ] PostgreSQL database (optional for testing)
- [ ] One of:
  - VS Code Copilot subscription OR
  - GitHub account (for GitHub Models free tier) OR
  - OpenAI API key

## 🚀 Installation (5 Minutes)

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/majidraza1228/mcp-toolkit.git
cd mcp-toolkit

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 3: Choose Your LLM Provider

Edit `.env` and choose ONE of these options:

#### Option A: VS Code Copilot / GitHub Models (RECOMMENDED)

```bash
LLM_PROVIDER=github
GITHUB_TOKEN=ghp_your_token_here
GITHUB_MODELS_API_KEY=${GITHUB_TOKEN}
LLM_MODEL=gpt-4o
DATABASE_URL=postgresql://localhost/mydb
```

**Get GitHub Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`, `read:org`
4. Copy token (starts with `ghp_`)

#### Option B: OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk_your_openai_key_here
GITHUB_TOKEN=ghp_your_token_here
LLM_MODEL=gpt-4
DATABASE_URL=postgresql://localhost/mydb
```

#### Option C: Anthropic Claude

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant_your_key_here
GITHUB_TOKEN=ghp_your_token_here
LLM_MODEL=claude-3-5-sonnet-20241022
DATABASE_URL=postgresql://localhost/mydb
```

### Step 4: Run!

```bash
python run.py
```

This will:
- ✅ Check your environment setup
- ✅ Test MCP server connections
- ✅ Launch the web UI at http://localhost:7860

## 🎨 Using the Web Interface

Once the UI loads:

1. **Server Status**: Check that Postgres and GitHub servers are connected
2. **Ask Questions**: Type in natural language
3. **See Results**: Agent will use the appropriate tools and show results

### Example Queries to Try

```
"List all tables in my database"
"Show me my GitHub repositories"
"How many users are in the database?"
"Create a GitHub issue titled 'Test Issue'"
"Find all active users and check their GitHub profiles"
```

## 📚 Next Steps

### Learn More
- [VSCODE_COPILOT_SETUP.md](VSCODE_COPILOT_SETUP.md) - Detailed GitHub Models setup
- [QUICKSTART.md](QUICKSTART.md) - Additional setup options
- [ARCHITECTURE.md](ARCHITECTURE.md) - How it all works
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details

### Run Examples

```bash
# Basic queries
python examples/basic_query.py

# Streaming responses
python examples/streaming_example.py

# Multi-step workflows
python examples/multi_step_task.py

# Direct tool calls (no LLM)
python examples/direct_tool_call.py
```

### Customize

1. **Add More MCP Servers**: Edit `mcp_config.json`
2. **Change Agent Behavior**: Edit `utils/prompts.py`
3. **Switch LLM Providers**: Change `LLM_PROVIDER` in `.env`

## 🔧 Troubleshooting

### "No LLM provider configured"

**Fix:** Make sure `.env` has `LLM_PROVIDER` set:
```bash
LLM_PROVIDER=github  # or openai, or anthropic
```

### "GitHub Models requires GITHUB_MODELS_API_KEY"

**Fix:** Set in `.env`:
```bash
GITHUB_MODELS_API_KEY=ghp_your_token_here
```

### "MCP server connection failed"

**Test manually:**
```bash
# Test Postgres server
npx @modelcontextprotocol/server-postgres postgresql://localhost/mydb

# Test GitHub server
GITHUB_TOKEN=your_token npx @modelcontextprotocol/server-github
```

### "Database connection failed"

**Fix:**
```bash
# Make sure PostgreSQL is running
pg_isready

# Test connection
psql postgresql://localhost/mydb
```

### Port 7860 already in use

**Fix:** Change port in `ui_client.py`:
```python
ui.launch(server_port=8080)  # Use different port
```

## 💡 Tips

### For VS Code Copilot Users
- ✅ Use your existing GitHub token
- ✅ Set `LLM_PROVIDER=github`
- ✅ Choose `gpt-4o` for best results
- ✅ No extra API costs!

### Cost Optimization
- Use `gpt-3.5-turbo` for simple queries (cheaper)
- Use `gpt-4o` for complex reasoning
- Set `LLM_TEMPERATURE=0` for consistent results
- Cache frequently asked questions

### Performance
- Use `LLM_PROVIDER=groq` for ultra-fast responses
- Enable streaming for better UX
- Consider running MCP servers over HTTP (not stdio) for production

## 🎉 You're Ready!

Your AI agent is now running and ready to:
- ✅ Answer questions about your database
- ✅ Manage GitHub repositories
- ✅ Execute complex workflows
- ✅ All in natural language!

**Start chatting with your agent at http://localhost:7860**

---

## Quick Reference

| Task | Command |
|------|---------|
| **Run application** | `python run.py` |
| **Run examples** | `python examples/basic_query.py` |
| **Test agent only** | `python agent_service.py` |
| **Test UI only** | `python ui_client.py` |
| **Check environment** | `cat .env \| grep -E "LLM_PROVIDER\|GITHUB\|OPENAI"` |

## Need Help?

1. Check [VSCODE_COPILOT_SETUP.md](VSCODE_COPILOT_SETUP.md) for LLM setup
2. Read [TROUBLESHOOTING.md](README.md#troubleshooting) section
3. Open an issue: https://github.com/majidraza1228/mcp-toolkit/issues

Happy building! 🚀
