# MCP Toolkit - Claude Code Context

## Project Summary

Standalone Python web app providing a natural-language AI agent that connects to databases, GitHub, and filesystems via the Model Context Protocol (MCP). Runs at `http://localhost:7860` (no VS Code required).

## Tech Stack

- **Python 3.11+** / async-first (`asyncio`, `async for`)
- **Gradio** - Web UI framework
- **LangChain** - LLM abstraction (OpenAI, Anthropic)
- **mcp-use** - MCP client library (`MCPAgent`)
- **Node.js** - MCP server processes (npx)

## Key Commands

```bash
./start.sh          # Start the app (launches MCP servers + Gradio UI)
./stop.sh           # Stop all processes
python run.py       # Alternative start (with env checks)
python run_eval.py  # Run evaluation suite
python run_eval.py --quick              # Easy tests only
python run_eval.py --category github    # Filter by category
python run_eval.py --difficulty hard    # Filter by difficulty
```

## Architecture

```
Browser (:7860) → ui_client.py (Gradio) → agent_service.py (AgentService)
                                              ├─ Standard mode (MCPAgent.stream)
                                              ├─ A2A mode (A2AOrchestrator.stream)
                                              └─ Agentic mode (AgenticLoop.run)
                                                    ↓
                                           utils/mcp_manager.py (MCPManager)
                                                    ↓  MCP Protocol (stdio/JSON-RPC)
                                           ┌────────┼────────┐
                                        postgres  github  filesystem
```

## File Map

| File | Purpose |
|------|---------|
| `run.py` | Entry point - env validation, launches UI |
| `ui_client.py` | Gradio web interface, chat handling, event loop bridge |
| `agent_service.py` | Core agent - LLM setup, streaming, 3 execution modes |
| `mcp_config.json` | MCP server definitions (postgres, github, filesystem) |
| `utils/mcp_manager.py` | MCP client connections, config loading, tool routing |
| `utils/prompts.py` | System prompt generation |
| `utils/simple_memory.py` | Query caching (MD5), feedback tracking, persistent JSON |
| `utils/a2a_orchestrator.py` | Multi-agent orchestration (GitHub/DB/FS specialists) |
| `utils/agentic_loop.py` | Plan-Act-Observe-Reflect pattern with SubGoal tracking |
| `utils/eval_framework.py` | 6 LLM metrics (correctness, relevance, faithfulness, completeness, consistency, safety) |
| `utils/business_evals.py` | Business-specific evaluation cases |
| `run_eval.py` | CLI evaluation runner |
| `eval_results.json` | Latest eval results |
| `AGENTS.md` | AI agent guidelines (for non-Claude-Code AI tools) |
| `docs/` | Detailed documentation (architecture, providers, A2A, etc.) |

## Coding Standards

- PEP 8 with type hints on all public methods
- Async/await for all I/O (MCP calls, LLM calls)
- `Optional[T]` for nullable params, `Dict`/`List` from `typing`
- Docstrings: Google style with Args/Returns sections
- Environment variables via `python-dotenv` (`.env` file, gitignored)

## Configuration (.env)

```
LLM_PROVIDER=openai|github|anthropic
LLM_MODEL=gpt-4|gpt-4o-mini|claude-3-5-sonnet-20241022
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GITHUB_TOKEN=...
DATABASE_URL=postgresql://...
A2A_ENABLED=true|false
AGENTIC_MODE=true|false
```

## Streaming Pattern (3 code paths in agent_service.py `stream()`)

All three paths follow the same pattern:
```python
full_response = ""
async for chunk in <source>.stream(query):
    if isinstance(chunk, str):
        full_response += chunk    # MUST use += (not =)
    yield chunk
if full_response:
    self.memory.save_query_response(query, full_response)
```

Sources: `self.agentic_loop.run()`, `self.a2a_orchestrator.stream()`, `self.agent.stream()`

## Common Pitfalls

- **Response concatenation**: All 3 streaming paths must use `full_response += chunk` (not `=`), or only the last chunk gets cached
- **Server binding**: UI server must bind to `127.0.0.1` (not `0.0.0.0`) since there is no authentication
- **GitHub Models limit**: 8K token context window - queries may silently truncate
- **MCP server lifecycle**: Servers are child processes; they die if the parent Python process dies
- **Async bridge**: `ui_client.py` bridges sync Gradio callbacks to async agent calls via `loop.run_until_complete()`

## Detailed Docs

- `docs/ARCHITECTURE.md` - Component architecture and data flow
- `docs/LLM_PROVIDERS.md` - Provider setup (GitHub free, OpenAI, Anthropic)
- `docs/A2A_GUIDE.md` - Agent-to-Agent orchestration
- `docs/EVALUATION_FRAMEWORK.md` - Eval metrics and procedures
- `docs/LEARNING_SYSTEM.md` - Self-learning / caching system
- `docs/TESTING_GUIDE.md` - Testing procedures
