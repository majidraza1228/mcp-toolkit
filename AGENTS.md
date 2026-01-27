# AI Agent Guidelines for MCP Toolkit

This document provides rules and context for AI assistants (GitHub Copilot, Claude, Cursor, etc.) working with this codebase.

## Project Overview

MCP Toolkit is a **standalone web application** that connects AI agents to databases, APIs, and file systems using the Model Context Protocol (MCP). It runs in a browser at `http://localhost:7860` - **no VS Code or IDE required**.

## Architecture

```
Browser (Gradio UI)
    ↓
Python Application (run.py, ui_client.py, agent_service.py)
    ↓
MCP Client (mcp-use library)
    ↓
MCP Servers (Node.js processes via npx)
    ├── @modelcontextprotocol/server-github
    ├── @modelcontextprotocol/server-postgres
    └── @modelcontextprotocol/server-filesystem
```

## Key Files

| File | Purpose |
|------|---------|
| `run.py` | Main entry point, environment checks, launches UI |
| `ui_client.py` | Gradio web interface |
| `agent_service.py` | LLM integration, MCP agent orchestration |
| `utils/mcp_manager.py` | MCP client connection management |
| `utils/prompts.py` | System prompts for the AI agent |
| `utils/simple_memory.py` | Query caching and learning system |
| `utils/a2a_orchestrator.py` | A2A (Agent-to-Agent) orchestration |
| `utils/agentic_loop.py` | Plan-Act-Observe-Reflect agentic pattern |
| `utils/eval_framework.py` | Agent evaluation and testing framework |
| `run_eval.py` | CLI tool to run agent evaluations |
| `docs/TESTING_GUIDE.md` | Comprehensive testing documentation |
| `mcp_config.json` | MCP server configuration |
| `.env` | Environment variables (API keys, database URL) |

## Configuration Rules

### Environment Variables (.env)

```bash
# LLM Provider - MUST be one of: github, openai, anthropic
LLM_PROVIDER=github|openai|anthropic

# Model selection based on provider:
# - github: Use gpt-4o-mini ONLY (8K token limit)
# - openai: gpt-4, gpt-4o, gpt-4-turbo, gpt-3.5-turbo
# - anthropic: claude-sonnet-4-20250514, claude-opus-4-20250514
LLM_MODEL=<model-name>

# A2A (Agent-to-Agent) mode
A2A_ENABLED=true|false

# Agentic Loop (Plan-Act-Observe-Reflect)
AGENTIC_MODE=true|false

# Required tokens/keys
GITHUB_TOKEN=ghp_...        # Always required for GitHub MCP server
OPENAI_API_KEY=sk-...       # Required if LLM_PROVIDER=openai
ANTHROPIC_API_KEY=sk-ant-...# Required if LLM_PROVIDER=anthropic
DATABASE_URL=postgresql://... # Required for postgres MCP server
```

### MCP Configuration (mcp_config.json)

- Only servers in `mcpServers` object are active
- Disabled servers go in `_disabled_servers`
- Environment variables use `${VAR_NAME}` syntax
- **GitHub Models (free) limitation**: Use only 1 MCP server due to 8K token limit

```json
{
  "mcpServers": {
    "server_name": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-name", "..."],
      "env": { "TOKEN": "${ENV_VAR}" }
    }
  }
}
```

## Coding Standards

### Python

- **Version**: Python 3.11+ required (mcp-use library requirement)
- **Style**: Follow PEP 8
- **Type hints**: Use type hints for function signatures
- **Async**: MCP operations are async - use `async/await`
- **Imports**: Group standard library, third-party, local imports

### Error Handling

```python
# Good - specific error handling
try:
    result = await mcp_client.call_tool(name, args)
except McpError as e:
    logger.error(f"MCP tool failed: {e}")
    raise

# Bad - swallowing errors
try:
    result = await mcp_client.call_tool(name, args)
except:
    pass
```

### Environment Variables

```python
# Good - use dotenv and provide defaults
from dotenv import load_dotenv
load_dotenv()

provider = os.getenv("LLM_PROVIDER", "openai").lower()

# Bad - no default, no case handling
provider = os.environ["LLM_PROVIDER"]
```

## Common Tasks

### Adding a New MCP Server

1. Add to `mcp_config.json` under `mcpServers`
2. Add any required env vars to `.env.example`
3. Update documentation in `docs/LLM_PROVIDERS.md`

### Adding a New LLM Provider

1. Update `agent_service.py` `_create_llm()` method
2. Update `run.py` `check_environment()` function
3. Update `ui_client.py` `get_llm_info()` method
4. Add to `docs/LLM_PROVIDERS.md`

### Modifying the UI

- UI is in `ui_client.py` using Gradio
- Theme is dark mode by default
- Server status panel is on the right
- Chat interface is on the left

## Testing

```bash
# Start the application
./start.sh

# View logs
tail -f /tmp/mcp_app.log

# Stop the application
./stop.sh
```

## Important Constraints

### Token Limits (GitHub Models - Free Tier)

- **8K total tokens** (prompt + response)
- Each MCP server adds ~2-4K tokens for tool definitions
- Use only 1 MCP server at a time with GitHub Models
- Use `gpt-4o-mini` model only

### MCP Server Lifecycle

- Servers are spawned as child processes via `npx`
- Communication is via stdio (stdin/stdout)
- Servers must be restarted when `.env` changes
- Use `./stop.sh && ./start.sh` to restart

### Security

- Never commit `.env` file (contains API keys)
- `.env` is in `.gitignore`
- Sensitive data should use environment variables
- Database credentials should not be hardcoded

## Troubleshooting

### "Authentication Failed" for GitHub operations

1. Check `GITHUB_TOKEN` is valid: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`
2. Token needs `repo` scope for write operations
3. Restart app after changing token: `./stop.sh && ./start.sh`

### "tokens_limit_reached" error

1. Using GitHub Models (free) with too many MCP servers
2. Solution: Use only 1 server in `mcp_config.json`
3. Or switch to OpenAI/Anthropic provider

### Server won't start

1. Check Python version: `python3.11 --version`
2. Check Node.js: `node --version`
3. Check required env vars in `.env`
4. View logs: `tail -20 /tmp/mcp_app.log`

## Do NOT

- Do not hardcode API keys or tokens
- Do not commit `.env` file
- Do not use synchronous calls for MCP operations
- Do not assume VS Code is available (standalone app)
- Do not use Claude models with GitHub Models provider (not supported)
- Do not enable multiple MCP servers with GitHub Models (token limit)

## Do

- Use environment variables for all secrets
- Use async/await for MCP operations
- Restart app after config changes
- Check logs when debugging
- Follow existing code patterns
- Update documentation when adding features
