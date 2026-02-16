# Product Requirements Document (PRD)

## MCP Toolkit - AI Agent with Database & API Access

| Field | Value |
|-------|-------|
| **Product Name** | MCP Toolkit |
| **Version** | 2.0 |
| **Author** | Majid Raza |
| **Last Updated** | 2026-02-16 |
| **Status** | Active Development |
| **Repository** | https://github.com/majidraza1228/mcp-toolkit |

---

## 1. Executive Summary

MCP Toolkit is a standalone, browser-based AI agent application that connects to databases, APIs, and file systems through the Model Context Protocol (MCP). Users interact with their data sources using natural language through a Gradio-powered web chat interface at `http://localhost:7860`. The system supports multiple LLM providers, self-learning through query caching and user feedback, multi-agent orchestration (A2A), and an advanced agentic reasoning loop. No IDE or VS Code installation is required.

---

## 2. Problem Statement

### Current Pain Points

1. **Data Access Fragmentation**: Teams use separate tools (pgAdmin, GitHub UI, file explorers) to interact with different data sources, requiring context-switching and domain-specific knowledge (SQL, API syntax, etc.).
2. **Repetitive Queries**: Common data lookups are performed repeatedly with the same latency cost each time, wasting time and API tokens.
3. **Complex Multi-Source Queries**: Queries that span multiple data sources (e.g., "find all repos whose owners exist in the employees database") require manual orchestration across tools.
4. **Lack of Quality Measurement**: Most AI agent deployments lack systematic evaluation of response quality, safety, and consistency.

### Target Users

- **Developers** who need quick access to databases, GitHub repos, and local files without switching between tools
- **Data Analysts** who want to query databases using natural language instead of SQL
- **Team Leads / DevOps** who need cross-domain queries (GitHub + DB + filesystem) for auditing and reporting
- **AI Engineers** building and evaluating agent-based systems who need a reference implementation

---

## 3. Product Vision

**Enable anyone to interact with databases, APIs, and file systems through natural language, with an AI agent that learns from feedback and improves over time.**

### Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Cache hit rate (after 100+ queries) | > 50% | 50-80% (on track) |
| Response time (cached) | < 200ms | ~100ms |
| Response time (fresh) | < 5s | 2-3s |
| Eval pass rate | > 80% | 14.3% (needs improvement - token limit issues) |
| Safety score | 100% | 100% |
| User feedback ratio (positive:negative) | > 4:1 | Tracking |

---

## 4. Functional Requirements

### 4.1 Core Chat Interface

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1.1 | Web-based chat UI accessible at `http://localhost:7860` | P0 | Done |
| FR-1.2 | Natural language input with 2-10 line text box | P0 | Done |
| FR-1.3 | Streaming response display in real-time | P0 | Done |
| FR-1.4 | Conversation history maintained within session | P0 | Done |
| FR-1.5 | Clear conversation button | P1 | Done |
| FR-1.6 | Example queries for onboarding | P1 | Done |
| FR-1.7 | Professional dark theme UI | P2 | Done |
| FR-1.8 | Mobile-responsive layout | P2 | Done |

### 4.2 MCP Server Integration

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-2.1 | PostgreSQL MCP server - natural language SQL queries | P0 | Done |
| FR-2.2 | GitHub MCP server - repo, issue, PR, code search | P0 | Done |
| FR-2.3 | Filesystem MCP server - file read, search, directory listing | P1 | Done |
| FR-2.4 | MCP server selector dropdown (all/postgres/github/filesystem) | P1 | Done |
| FR-2.5 | Server status panel showing connection health and tool counts | P1 | Done |
| FR-2.6 | Automatic server-specific query routing via prompt injection | P1 | Done |
| FR-2.7 | Support for adding custom MCP servers via `mcp_config.json` | P1 | Done |
| FR-2.8 | Environment variable substitution in MCP config (`${VAR_NAME}`) | P1 | Done |

### 4.3 LLM Provider Support

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-3.1 | OpenAI GPT models (GPT-4, GPT-4o, GPT-4-turbo, GPT-3.5-turbo) | P0 | Done |
| FR-3.2 | Anthropic Claude models (Claude Sonnet 4, Claude Opus 4) | P0 | Done |
| FR-3.3 | GitHub Models free tier (GPT-4o-mini via Azure endpoint) | P1 | Done |
| FR-3.4 | Runtime provider switching via `.env` configuration | P1 | Done |
| FR-3.5 | LLM provider and model displayed in UI header | P2 | Done |

### 4.4 Self-Learning System

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-4.1 | Query caching with MD5 hash-based lookup | P0 | Done |
| FR-4.2 | User feedback buttons (thumbs up / thumbs down) | P0 | Done |
| FR-4.3 | Quality-gated cache retrieval (positive > negative feedback) | P0 | Done |
| FR-4.4 | Persistent memory storage in `memory_cache.json` | P0 | Done |
| FR-4.5 | Learning statistics dashboard (cached queries, hit rate, feedback counts) | P1 | Done |
| FR-4.6 | Cache v2.0 format with metadata, categories, tags, feedback scores | P1 | Done |
| FR-4.7 | Automatic v1.0 to v2.0 cache migration | P2 | Done |
| FR-4.8 | Query categorization (database_queries, schema_operations, etc.) | P2 | Done |

### 4.5 A2A (Agent-to-Agent) Orchestration

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-5.1 | Query analysis to identify target domains (GitHub, DB, Filesystem) | P0 | Done |
| FR-5.2 | Specialized agents for each domain | P0 | Done |
| FR-5.3 | Parallel execution of independent sub-tasks | P1 | Done |
| FR-5.4 | Result combination from multiple agents | P1 | Done |
| FR-5.5 | Fallback to standard mode on A2A errors | P1 | Done |
| FR-5.6 | A2A status badge in UI header | P2 | Done |
| FR-5.7 | Enable/disable via `A2A_ENABLED` env var | P1 | Done |

### 4.6 Agentic Loop (Plan-Act-Observe-Reflect)

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-6.1 | Planning phase - break complex queries into sub-goals | P0 | Done |
| FR-6.2 | Action phase - execute tools toward current sub-goal | P0 | Done |
| FR-6.3 | Observation phase - validate step results | P0 | Done |
| FR-6.4 | Reflection phase - analyze success/failure and adjust | P0 | Done |
| FR-6.5 | Self-correction with configurable max retries | P1 | Done |
| FR-6.6 | Agentic mode checkbox in UI (per-query toggle) | P1 | Done |
| FR-6.7 | Enable/disable via `AGENTIC_MODE` env var | P1 | Done |
| FR-6.8 | Fallback to standard mode on agentic errors | P1 | Done |

### 4.7 Evaluation Framework

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-7.1 | 6 core LLM metrics: Correctness, Relevance, Faithfulness, Completeness, Consistency, Safety | P0 | Done |
| FR-7.2 | Operational metrics: Tool Accuracy, Result Accuracy, Efficiency, Latency | P0 | Done |
| FR-7.3 | Pre-defined test cases for GitHub, Database, and Multi-domain queries | P0 | Done |
| FR-7.4 | CLI runner with `--quick`, `--category`, `--difficulty` filters | P1 | Done |
| FR-7.5 | JSON report output (`eval_results.json`) | P1 | Done |
| FR-7.6 | Custom `EvalCase` creation API | P1 | Done |
| FR-7.7 | Business-specific evaluation templates (finance, healthcare, etc.) | P2 | Done |
| FR-7.8 | CI/CD integration with exit codes (0 = pass >= 70%, 1 = fail) | P2 | Done |
| FR-7.9 | Safety detection: exposed secrets, destructive commands, bias indicators | P1 | Done |

---

## 5. Non-Functional Requirements

### 5.1 Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1.1 | Cached response time | < 200ms |
| NFR-1.2 | Fresh query response time | < 5 seconds |
| NFR-1.3 | UI load time | < 3 seconds |
| NFR-1.4 | Concurrent users (local deployment) | 1-5 |
| NFR-1.5 | Memory footprint | < 500MB |

### 5.2 Security

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-2.1 | Web server binds to `127.0.0.1` only (localhost) | Done |
| NFR-2.2 | API keys stored in `.env` file (gitignored) | Done |
| NFR-2.3 | No hardcoded credentials in source code | Done |
| NFR-2.4 | MCP servers run as local child processes | Done |
| NFR-2.5 | All data stays on the user's machine | Done |
| NFR-2.6 | Eval framework detects exposed secrets in responses | Done |
| NFR-2.7 | Input validation on chat text box (max 10 lines) | Done |

### 5.3 Reliability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-3.1 | Graceful error handling with user-friendly messages | Done |
| NFR-3.2 | Recursion limit handling (max 30 steps) | Done |
| NFR-3.3 | A2A → Standard mode fallback on error | Done |
| NFR-3.4 | Agentic → Standard mode fallback on error | Done |
| NFR-3.5 | Persistent cache survives application restarts | Done |

### 5.4 Compatibility

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-4.1 | Python 3.11+ | Required |
| NFR-4.2 | Node.js (for MCP servers via npx) | Required |
| NFR-4.3 | Any modern web browser | Required |
| NFR-4.4 | macOS, Linux support | Done |
| NFR-4.5 | No VS Code or IDE dependency | Done |

### 5.5 Observability (Optional)

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-5.1 | Langfuse integration for tracing | Optional |
| NFR-5.2 | LangSmith integration for tracing | Optional |
| NFR-5.3 | Application logs to `/tmp/mcp_app.log` | Done |

---

## 6. Architecture Overview

### 6.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                            │
│              http://localhost:7860                           │
│         (Gradio Web Interface - Chat UI)                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  PYTHON APPLICATION                          │
│                                                              │
│  ui_client.py ──→ agent_service.py ──→ utils/mcp_manager.py │
│  (Gradio UI)      (AgentService)       (MCPManager)         │
│                      │                                       │
│                      ├─ Standard Mode (MCPAgent.stream)      │
│                      ├─ A2A Mode (A2AOrchestrator.stream)    │
│                      └─ Agentic Mode (AgenticLoop.run)       │
│                                                              │
│  utils/simple_memory.py ──→ memory_cache.json                │
│  (Self-Learning Cache)                                       │
│                                                              │
│  utils/eval_framework.py ──→ eval_results.json               │
│  (Evaluation Engine)                                         │
└────────────────────┬────────────────────────────────────────┘
                     │ MCP Protocol (stdio / JSON-RPC)
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   ┌─────────┐ ┌──────────┐ ┌──────────┐
   │Postgres │ │  GitHub  │ │Filesystem│
   │MCP (npx)│ │MCP (npx) │ │MCP (npx) │
   └────┬────┘ └────┬─────┘ └────┬─────┘
        ↓            ↓            ↓
   PostgreSQL   GitHub API   Local Files
```

### 6.2 Execution Modes

| Mode | Trigger | Pattern | Best For |
|------|---------|---------|----------|
| **Standard** | Default, or single-server selected | ReAct (Reason + Act) | Simple lookups, single-domain queries |
| **A2A** | `A2A_ENABLED=true` + "all" servers | Multi-agent orchestration | Cross-domain queries, parallel tasks |
| **Agentic Loop** | `AGENTIC_MODE=true` or UI checkbox | Plan-Act-Observe-Reflect | Complex multi-step reasoning |

### 6.3 Data Flow (Streaming)

```
User Query
  → Check cache (SimpleMemory.get_cached_response)
    → Cache HIT: yield cached response, return
    → Cache MISS: continue
  → Select mode (Agentic → A2A → Standard)
  → Stream chunks:
      full_response = ""
      async for chunk in <mode>.stream(query):
          full_response += chunk   # accumulate
          yield chunk              # stream to UI
  → Save to cache (SimpleMemory.save_query_response)
```

---

## 7. Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Gradio | >= 4.0.0 | Web UI framework |
| **Backend** | Python | 3.11+ | Application runtime |
| **MCP Client** | mcp-use | >= 0.1.0 | MCP protocol client |
| **LLM Framework** | LangChain | >= 0.3.0 | LLM abstraction |
| **LLM Providers** | langchain-openai | >= 0.2.0 | OpenAI + GitHub Models |
| | langchain-anthropic | >= 0.2.0 | Anthropic Claude |
| **MCP Servers** | Node.js / npx | Latest | MCP server runtime |
| | @modelcontextprotocol/server-postgres | Latest | PostgreSQL MCP |
| | @modelcontextprotocol/server-github | Latest | GitHub MCP |
| | @modelcontextprotocol/server-filesystem | Latest | Filesystem MCP |
| **Database** | PostgreSQL | Any | Data source (optional) |
| **Config** | python-dotenv | >= 1.0.0 | Environment management |
| **HTTP** | aiohttp | >= 3.9.0 | Async HTTP client |

---

## 8. Configuration Reference

### 8.1 Environment Variables (`.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | Yes | `openai` | LLM provider: `github`, `openai`, `anthropic` |
| `LLM_MODEL` | No | Provider-dependent | Model name (e.g., `gpt-4`, `gpt-4o-mini`, `claude-sonnet-4-20250514`) |
| `OPENAI_API_KEY` | If provider=openai | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | If provider=anthropic | - | Anthropic API key |
| `GITHUB_TOKEN` | Yes (for GitHub MCP) | - | GitHub Personal Access Token (scopes: `repo`, `read:user`, `read:org`) |
| `DATABASE_URL` | For postgres MCP | - | PostgreSQL connection string |
| `A2A_ENABLED` | No | `true` | Enable A2A multi-agent orchestration |
| `AGENTIC_MODE` | No | `false` | Enable Agentic Loop (Plan-Act-Observe-Reflect) |

### 8.2 MCP Server Configuration (`mcp_config.json`)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
      "env": {}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {}
    }
  }
}
```

---

## 9. Key Files and Modules

| File | Lines | Responsibility |
|------|-------|----------------|
| `run.py` | ~80 | Entry point: env validation, launches UI |
| `ui_client.py` | ~555 | Gradio web interface, chat event handling, sync-async bridge |
| `agent_service.py` | ~445 | Core agent: LLM setup, 3 streaming modes, caching integration |
| `mcp_config.json` | ~20 | MCP server definitions |
| `utils/mcp_manager.py` | ~150 | MCP client connections, config loading, env substitution |
| `utils/prompts.py` | ~30 | System prompt generation |
| `utils/simple_memory.py` | ~300 | Query caching, feedback tracking, persistent JSON storage |
| `utils/a2a_orchestrator.py` | ~250 | A2A multi-agent orchestration |
| `utils/agentic_loop.py` | ~300 | Plan-Act-Observe-Reflect pattern |
| `utils/eval_framework.py` | ~500 | 6 LLM metrics + operational metrics evaluation |
| `utils/business_evals.py` | ~100 | Business-specific eval templates |
| `run_eval.py` | ~100 | CLI eval runner with filters |
| `start.sh` | ~20 | Application startup script |
| `stop.sh` | ~10 | Application shutdown script |

---

## 10. User Flows

### 10.1 Basic Query Flow

```
1. User opens http://localhost:7860
2. User types: "Show all tables in the database"
3. System checks cache → miss
4. System selects mode (A2A if enabled, else Standard)
5. Agent reasons about tools → selects postgres MCP `query` tool
6. MCP server executes: SELECT table_name FROM information_schema.tables
7. Response streams back to UI in real-time
8. Response cached in memory_cache.json
9. User clicks thumbs up → cache entry activated for future queries
```

### 10.2 Cached Query Flow

```
1. User types: "show all tables in the database" (similar to previous)
2. System generates MD5 hash → matches cache
3. Cache check: positive_feedback(1) > negative_feedback(0) → valid
4. Cached response returned instantly (~100ms)
5. Cache hit counter incremented
```

### 10.3 Multi-Agent Query Flow (A2A)

```
1. User types: "Find all repos and list database tables"
2. A2A orchestrator analyzes query → identifies GitHub + Database domains
3. Creates parallel task plan:
   - Task 1 → GitHub agent: "list repositories"
   - Task 2 → Database agent: "list database tables"
4. Both tasks execute in parallel
5. Results combined into unified response
6. Streamed to user
```

### 10.4 Agentic Loop Flow

```
1. User enables "Agentic Mode" checkbox
2. User types: "Find repos with open issues and summarize their database tables"
3. Planning phase: Breaks into 3 sub-goals
4. Step 1/3: Search repositories → Success
5. Step 2/3: List open issues per repo → Success
6. Step 3/3: Query database tables → Success
7. Reflection: All goals met, combining results
8. Final summary streamed to user
```

### 10.5 Evaluation Flow

```
1. Developer runs: python run_eval.py --quick
2. Framework loads pre-defined test cases (easy difficulty)
3. For each test case:
   a. Send query to agent
   b. Measure latency
   c. Compare actual tools vs expected tools
   d. Check response for expected keywords
   e. Score 6 core metrics + operational metrics
   f. Check safety (secrets, destructive commands, bias)
4. Generate report with pass/fail, metrics, and category breakdown
5. Save to eval_results.json
6. Exit code 0 if pass rate >= 70%, else exit code 1
```

---

## 11. Known Limitations and Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| GitHub Models 8K token limit | Context exceeds limit with 3+ MCP servers | Use only 1 server with free tier, or switch to paid provider |
| MD5 exact-match caching | Slight rephrasing misses cache | Planned: semantic similarity matching |
| No authentication on web UI | Anyone on localhost can access | Server bound to 127.0.0.1 only |
| MCP servers are child processes | Die when parent Python process dies | Managed via start.sh / stop.sh scripts |
| Single-user session model | Conversation history not persisted across restarts | Cache persists; conversation doesn't |
| Eval pass rate 14.3% | Most failures due to token limit on free tier | Use paid provider for proper evaluation |

---

## 12. Future Roadmap

### Phase 3.0 - Enhanced Intelligence

| Feature | Description | Priority |
|---------|-------------|----------|
| Semantic similarity caching | Use embeddings for fuzzy query matching instead of exact MD5 | P1 |
| Conversation persistence | Save and restore conversation history across sessions | P1 |
| Context-aware caching | Factor conversation history into cache decisions | P2 |
| Agent memory sharing | Cross-agent context passing in A2A mode | P2 |

### Phase 3.1 - Scale and Deployment

| Feature | Description | Priority |
|---------|-------------|----------|
| Authentication layer | Add login/session management for multi-user deployment | P1 |
| Docker containerization | One-command deployment with Docker Compose | P1 |
| Remote deployment | Deploy to cloud with HTTPS and proper auth | P2 |
| Multi-user cache isolation | Per-user cache partitioning | P2 |

### Phase 3.2 - Observability and Quality

| Feature | Description | Priority |
|---------|-------------|----------|
| Langfuse/LangSmith integration | Production tracing and debugging | P1 |
| Automated regression testing | CI/CD pipeline with eval gate | P1 |
| A/B testing | Compare cached vs fresh responses | P2 |
| Analytics dashboard | Detailed usage and learning visualizations | P2 |
| Confidence scores | Display confidence in cached responses | P2 |

### Phase 3.3 - Extensibility

| Feature | Description | Priority |
|---------|-------------|----------|
| Custom agent definitions | User-defined specialized agents for A2A | P2 |
| Plugin system for MCP servers | UI-based server management instead of JSON editing | P2 |
| Ollama local model support | Run models locally without API keys | P2 |
| Export/import learned patterns | Share caches across deployments | P3 |

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - an open standard for connecting AI models to data sources via stdio/JSON-RPC |
| **MCPAgent** | Agent class from the `mcp-use` library that combines an LLM with MCP tools |
| **A2A** | Agent-to-Agent orchestration - routing tasks to specialized domain agents |
| **Agentic Loop** | Plan-Act-Observe-Reflect pattern for multi-step reasoning with self-correction |
| **ReAct** | Reason + Act pattern - the standard single-step agent execution model |
| **Gradio** | Python library for building web UIs with ML/AI applications |
| **LangChain** | Framework for building LLM-powered applications with tool use and agents |
| **EvalCase** | A test case definition in the evaluation framework |

---

## 14. References

- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification
- [mcp-use Library](https://github.com/sparfenyuk/mcp-use) - MCP client for Python
- [Gradio](https://gradio.app) - Web UI framework
- [LangChain](https://langchain.com) - LLM framework
- [Architecture Overview](ARCHITECTURE.md) - Detailed system architecture
- [LLM Providers Guide](LLM_PROVIDERS.md) - Provider configuration
- [A2A Guide](A2A_GUIDE.md) - Multi-agent orchestration
- [Evaluation Framework](EVALUATION_FRAMEWORK.md) - Testing and metrics
- [Learning System](LEARNING_SYSTEM.md) - Self-learning documentation
