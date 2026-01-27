# A2A (Agent-to-Agent) Orchestration Guide

![A2A Mode Interface](./screenshots/image.png)
*MCP Toolkit with A2A Mode enabling multi-agent collaboration*

This guide explains the A2A (Agent-to-Agent) feature in MCP Toolkit, which enables multiple specialized AI agents to collaborate on complex tasks.

## Overview

A2A orchestration allows the system to:
- **Route tasks** to specialized agents based on the query type
- **Execute in parallel** when tasks are independent
- **Combine results** from multiple agents intelligently
- **Improve accuracy** through domain specialization

## Architecture

```
User Query
    ↓
┌─────────────────────────────────────┐
│        A2A Orchestrator             │
│  (Analyzes query, creates plan)     │
└─────────────────────────────────────┘
    ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│ GitHub  │ │Database │ │Filesystem│
│  Agent  │ │  Agent  │ │  Agent  │
└─────────┘ └─────────┘ └─────────┘
    ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│ GitHub  │ │Postgres │ │Filesystem│
│  MCP    │ │  MCP    │ │  MCP    │
└─────────┘ └─────────┘ └─────────┘
```

## Specialized Agents

### GitHub Agent
Specializes in:
- Repository management (create, fork, clone)
- Branch operations (create, merge, delete)
- Issue and PR management
- Code search and file operations
- User and organization queries

### Database Agent
Specializes in:
- SQL query construction
- Database schema analysis
- Data retrieval and aggregation
- Table relationships and joins

### Filesystem Agent
Specializes in:
- File and directory operations
- File content search
- Directory structure exploration
- File metadata queries

## How It Works

### 1. Query Analysis
When you submit a query, the orchestrator analyzes it to determine:
- Which agent(s) should handle it
- Whether tasks can run in parallel
- How to combine results

### 2. Task Routing
The orchestrator creates a task plan:
```json
{
  "tasks": [
    {"agent": "github", "query": "list repositories"},
    {"agent": "postgres", "query": "count users"}
  ],
  "parallel": true,
  "reasoning": "Independent queries, can run in parallel"
}
```

### 3. Execution
- **Parallel**: Independent tasks run simultaneously
- **Sequential**: Dependent tasks run in order

### 4. Result Combination
Results from all agents are combined into a unified response.

## Configuration

### Enable A2A Mode

In your `.env` file:
```bash
A2A_ENABLED=true
```

### Requirements

A2A mode works best with:
1. **Paid LLM Provider** (OpenAI or Anthropic) - More token headroom
2. **Multiple MCP Servers** - Enable all servers you need

### MCP Configuration for A2A

Enable all servers you need in `mcp_config.json`:
```json
{
  "mcpServers": {
    "github": { ... },
    "postgres": { ... },
    "filesystem": { ... }
  }
}
```

## Example Queries

### Single-Agent Queries
These are routed to one specialized agent:

| Query | Agent |
|-------|-------|
| "List my GitHub repos" | GitHub |
| "Show all tables in the database" | Database |
| "Find all Python files" | Filesystem |

### Multi-Agent Queries
These leverage multiple agents:

| Query | Agents |
|-------|--------|
| "Find repos with database schemas and show me the table structure" | GitHub + Database |
| "Compare file contents with database records" | Filesystem + Database |
| "Create a report of repos and their local clones" | GitHub + Filesystem |

## Performance Considerations

### Token Limits
- **GitHub Models (Free)**: Limited to 8K tokens - A2A may hit limits
- **OpenAI**: 128K tokens - Full A2A support
- **Anthropic**: 200K tokens - Full A2A support

### Parallel Execution
Parallel execution is faster but uses more tokens simultaneously.

### Fallback Behavior
If A2A encounters an error, it falls back to standard single-agent mode.

## UI Indicators

When A2A is active:
- Header shows "A2A Mode Active" badge
- Server status panel shows "A2A Mode: Active"
- Response indicates which agent(s) handled the query

## Troubleshooting

### A2A Not Activating
1. Check `A2A_ENABLED=true` in `.env`
2. Verify multiple MCP servers are configured
3. Check logs for initialization errors

### Token Limit Errors
1. Use a paid LLM provider (OpenAI/Anthropic)
2. Reduce the number of enabled MCP servers
3. Break complex queries into smaller parts

### Agent Routing Issues
1. Be specific in your queries
2. Mention the data source explicitly
3. Check that required servers are connected

## Disabling A2A

To disable A2A and use single-agent mode:
```bash
# In .env
A2A_ENABLED=false
```

Or select a specific server in the UI dropdown instead of "all".

## Best Practices

1. **Use specific queries** - Helps routing accuracy
2. **Enable only needed servers** - Reduces token usage
3. **Use paid providers for complex workflows** - More reliable
4. **Monitor the logs** - See which agents are handling queries

## Technical Details

### Files
- `utils/a2a_orchestrator.py` - Main orchestration logic
- `agent_service.py` - Integration with agent service

### Classes
- `A2AOrchestrator` - Main orchestrator class
- `SpecializedAgent` - Individual agent wrapper
- `AgentTask` - Task definition
- `AgentResult` - Execution result

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `A2A_ENABLED` | `true` | Enable/disable A2A mode |

## Related Documentation

- [AGENTIC_IMPROVEMENTS.md](AGENTIC_IMPROVEMENTS.md) - True agentic patterns and evaluation framework
- [A2A_VS_STANDARD.md](A2A_VS_STANDARD.md) - Comparison between A2A and Standard modes

## Future Enhancements

Planned features:
- Agent memory sharing
- Cross-agent context passing
- Custom agent definitions
- Agent performance metrics
- Agentic loop with Plan-Act-Observe-Reflect pattern
