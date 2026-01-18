# A2A vs Standard Mode Comparison

![A2A Mode Interface](./screenshots/image.png)
*MCP Toolkit with A2A Mode showing multiple specialized agents collaborating*

This document explains the differences between **A2A (Agent-to-Agent)** mode and **Standard** mode in MCP Toolkit.

## Overview

MCP Toolkit supports two execution modes:

| Mode | Description |
|------|-------------|
| **Standard** | Single general-purpose agent handles all queries |
| **A2A** | Multiple specialized agents collaborate on queries |

---

## Standard Mode (Without A2A)

### Architecture

```
User Query: "List GitHub repos and show database tables"
                    │
                    ▼
            ┌───────────────┐
            │  Single Agent │ ← One agent tries to do EVERYTHING
            └───────────────┘
                    │
                    ▼
         Connects to ALL servers
         sequentially, one by one
                    │
                    ▼
            Single Response
```

### How It Works

1. **Single Agent**: One general-purpose AI agent receives the query
2. **Tool Discovery**: Agent loads ALL available tools from ALL MCP servers
3. **Sequential Execution**: Agent executes tools one at a time
4. **Single Context**: All reasoning happens in one context window

### Characteristics

| Aspect | Standard Mode |
|--------|---------------|
| **Agents** | 1 general-purpose agent |
| **Execution** | Sequential |
| **Tool Loading** | All tools loaded at once |
| **Context** | Single context window |
| **Decision Making** | Agent decides everything |

### Example Flow

```
Query: "Show my GitHub repos and count database users"

Step 1: Agent receives query
Step 2: Agent thinks... "I need GitHub tools"
Step 3: Agent connects to GitHub MCP server
Step 4: Agent lists repositories
Step 5: Agent thinks... "Now I need database tools"
Step 6: Agent connects to Postgres MCP server
Step 7: Agent runs SQL COUNT query
Step 8: Agent combines and returns result

Total time: ~8-10 seconds (sequential)
```

### When to Use Standard Mode

- Simple, single-domain queries
- Limited token budget (GitHub Models free tier)
- Queries that only need one MCP server
- When you want direct control over server selection

### Configuration

```bash
# In .env
A2A_ENABLED=false
```

Or select a specific server in the UI dropdown instead of "all".

---

## A2A Mode (With Agent-to-Agent)

### Architecture

```
User Query: "List GitHub repos and show database tables"
                    │
                    ▼
            ┌───────────────┐
            │  Orchestrator │ ← Analyzes query, creates execution plan
            └───────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  GitHub   │ │ Database  │ │Filesystem │
│   Agent   │ │   Agent   │ │   Agent   │
│ (Expert)  │ │ (Expert)  │ │ (Expert)  │
└───────────┘ └───────────┘ └───────────┘
        │           │           │
        ▼           ▼           ▼
   GitHub MCP   Postgres MCP  Filesystem MCP
        │           │           │
        └───────────┼───────────┘
                    ▼
            Combined Response
```

### How It Works

1. **Query Analysis**: Orchestrator analyzes the user query
2. **Task Planning**: Creates a plan with tasks for each relevant agent
3. **Parallel Routing**: Routes tasks to specialized agents
4. **Expert Execution**: Each agent executes in its domain
5. **Result Combination**: Orchestrator combines all results

### Orchestrator Planning

The orchestrator creates a JSON execution plan:

```json
{
  "tasks": [
    {
      "agent": "github",
      "query": "list user repositories",
      "priority": 1,
      "depends_on": []
    },
    {
      "agent": "postgres",
      "query": "count users in database",
      "priority": 1,
      "depends_on": []
    }
  ],
  "parallel": true,
  "reasoning": "Independent queries can run in parallel"
}
```

### Specialized Agents

#### GitHub Agent
```
Expertise:
├── Repository management (create, fork, clone)
├── Branch operations (create, merge, delete)
├── Issue and PR management
├── Code search and file operations
└── User and organization queries
```

#### Database Agent
```
Expertise:
├── SQL query construction
├── Database schema analysis
├── Data retrieval and aggregation
├── Table relationships and joins
└── Data integrity checks
```

#### Filesystem Agent
```
Expertise:
├── File and directory operations
├── File content search
├── Directory structure exploration
└── File metadata queries
```

### Characteristics

| Aspect | A2A Mode |
|--------|----------|
| **Agents** | Multiple specialized experts |
| **Execution** | Parallel (when possible) |
| **Tool Loading** | Distributed per agent |
| **Context** | Separate context per agent |
| **Decision Making** | Orchestrator plans, agents execute |

### Example Flow

```
Query: "Show my GitHub repos and count database users"

Step 1: Orchestrator analyzes query
Step 2: Creates plan: GitHub Agent + Database Agent (parallel)
Step 3: GitHub Agent → Lists repos    ┐
Step 4: Database Agent → Counts users ┘ (PARALLEL)
Step 5: Results combined by orchestrator
Step 6: Returns unified response

Total time: ~4-5 seconds (parallel execution)
```

### When to Use A2A Mode

- Complex multi-domain queries
- Queries spanning multiple data sources
- When speed matters (parallel execution)
- Paid LLM providers with large context windows

### Configuration

```bash
# In .env
A2A_ENABLED=true
LLM_PROVIDER=openai  # or anthropic (need large context)
```

Enable all servers in `mcp_config.json`:
```json
{
  "mcpServers": {
    "github": { ... },
    "postgres": { ... },
    "filesystem": { ... }
  }
}
```

---

## Side-by-Side Comparison

### Feature Comparison

| Feature | Standard Mode | A2A Mode |
|---------|---------------|----------|
| **Number of Agents** | 1 | 3+ (specialized) |
| **Execution Pattern** | Sequential | Parallel |
| **Query Routing** | Agent decides | Orchestrator plans |
| **Domain Expertise** | General | Specialized |
| **Speed (multi-domain)** | Slower | Faster |
| **Accuracy** | Good | Better |
| **Token Usage** | All at once | Distributed |
| **Error Handling** | Single point | Per domain |
| **Complexity** | Simple | More sophisticated |

### Performance Comparison

| Query Type | Standard | A2A |
|------------|----------|-----|
| Single domain | ~3-4s | ~3-4s |
| Two domains | ~6-8s | ~4-5s |
| Three domains | ~9-12s | ~5-6s |
| Complex multi-step | ~15-20s | ~8-10s |

### Token Usage

| Scenario | Standard | A2A |
|----------|----------|-----|
| Tool definitions | All loaded (~8K) | Per agent (~2-3K each) |
| Context window | Single large | Multiple smaller |
| GitHub Models compatible | Limited | No (too many tokens) |
| OpenAI/Anthropic | Full support | Full support |

---

## Query Examples

### Single-Domain Queries (Both modes work similarly)

| Query | Routed To |
|-------|-----------|
| "List my GitHub repositories" | GitHub Agent |
| "Show all database tables" | Database Agent |
| "Find all Python files" | Filesystem Agent |

### Multi-Domain Queries (A2A shines here)

| Query | A2A Routing |
|-------|-------------|
| "Show repos and database schema" | GitHub + Database (parallel) |
| "Compare file structure with DB tables" | Filesystem + Database |
| "Find repos with matching local files" | GitHub + Filesystem |
| "Full system report" | All 3 agents (parallel) |

### Complex Queries

**Query**: "List my active GitHub repos, count users in each related database table, and show the Python files in this project"

**Standard Mode**:
```
1. Connect to GitHub → List repos (3s)
2. Connect to Postgres → Count users (3s)
3. Connect to Filesystem → Find Python files (2s)
Total: ~8s (sequential)
```

**A2A Mode**:
```
1. Orchestrator analyzes → Creates 3-task plan
2. GitHub Agent → repos     ┐
3. Database Agent → counts  ├── All parallel
4. Filesystem Agent → files ┘
5. Combine results
Total: ~4s (parallel)
```

---

## UI Indicators

### Standard Mode
- Header shows LLM provider only
- Server status panel shows "A2A Mode: Disabled"
- Dropdown allows specific server selection

### A2A Mode
- Header shows "🔄 A2A" badge
- "A2A Mode Active" highlighted in green
- Server status shows all specialized agents
- Response indicates which agent(s) handled query

---

## Switching Between Modes

### Enable A2A
```bash
# .env
A2A_ENABLED=true
```

### Disable A2A
```bash
# .env
A2A_ENABLED=false
```

### Temporary Override
Select a specific server in the UI dropdown (e.g., "github" instead of "all") to bypass A2A for that query.

---

## Best Practices

### Use Standard Mode When:
- Using GitHub Models (free tier) - 8K token limit
- Simple, single-source queries
- You want explicit control over which server handles the query
- Debugging or testing specific MCP servers

### Use A2A Mode When:
- Using OpenAI or Anthropic (large context windows)
- Complex queries spanning multiple data sources
- Speed is important
- You want intelligent automatic routing

---

## Troubleshooting

### A2A Not Working

1. Check `A2A_ENABLED=true` in `.env`
2. Verify multiple MCP servers are configured
3. Ensure using paid LLM provider (OpenAI/Anthropic)
4. Check logs: `tail -f /tmp/mcp_app.log`

### Slow A2A Performance

1. Check network connectivity to all services
2. Verify database connection is fast
3. Consider if query truly needs multiple agents

### Falling Back to Standard

If A2A encounters errors, it automatically falls back to standard mode with a warning message.

---

## Summary

| If You Want... | Use |
|----------------|-----|
| Simple queries, free tier | Standard Mode |
| Complex multi-domain queries | A2A Mode |
| Maximum speed | A2A Mode |
| Explicit server control | Standard Mode |
| Best accuracy for complex tasks | A2A Mode |

**Recommendation**: If you have an OpenAI or Anthropic API key, enable A2A for the best experience with complex queries.
