# Architecture Guide

Complete architectural overview of the Python Full-Stack MCP Application.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Gradio Web UI (ui_client.py)                          │     │
│  │  - Chat interface                                      │     │
│  │  - Server status dashboard                             │     │
│  │  - Example queries                                     │     │
│  │  Port: 7860                                            │     │
│  └─────────────────────┬──────────────────────────────────┘     │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI AGENT SERVICE LAYER                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  AgentService (agent_service.py)                       │     │
│  │  ┌──────────────────────────────────────────────┐     │     │
│  │  │  MCPAgent (from mcp-use library)             │     │     │
│  │  │  - Natural language processing               │     │     │
│  │  │  - Multi-step reasoning                      │     │     │
│  │  │  - Tool selection & execution                │     │     │
│  │  │  - Conversation memory                       │     │     │
│  │  └──────────────────┬───────────────────────────┘     │     │
│  │                     │                                  │     │
│  │                     ▼                                  │     │
│  │  ┌──────────────────────────────────────────────┐     │     │
│  │  │  LLM (LangChain)                             │     │     │
│  │  │  - OpenAI GPT-4                              │     │     │
│  │  │  - Anthropic Claude                          │     │     │
│  │  │  - Groq / Local models                       │     │     │
│  │  └──────────────────────────────────────────────┘     │     │
│  └─────────────────────┬──────────────────────────────────┘     │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP CLIENT MANAGER LAYER                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  MCPManager (utils/mcp_manager.py)                     │     │
│  │  ┌──────────────────────────────────────────────┐     │     │
│  │  │  MCPClient (from mcp-use library)            │     │     │
│  │  │  - Session management                        │     │     │
│  │  │  - Connection pooling                        │     │     │
│  │  │  - Tool discovery                            │     │     │
│  │  │  - Resource access                           │     │     │
│  │  └──────────┬────────────┬──────────────┬───────┘     │     │
│  └─────────────┼────────────┼──────────────┼─────────────┘     │
└────────────────┼────────────┼──────────────┼───────────────────┘
                 │            │              │
                 ▼            ▼              ▼
┌────────────────────────────────────────────────────────────────┐
│                    MCP SERVERS LAYER (Node.js)                 │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Postgres    │  │   GitHub     │  │   Filesystem     │    │
│  │  MCP Server  │  │  MCP Server  │  │   MCP Server     │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────────┤    │
│  │ Tools:       │  │ Tools:       │  │ Tools:           │    │
│  │ - query      │  │ - list_repos │  │ - read_file      │    │
│  │ - execute    │  │ - create_issue│ │ - write_file     │    │
│  │ - schema     │  │ - get_user   │  │ - list_dir       │    │
│  │              │  │ - search     │  │ - search         │    │
│  │ Resources:   │  │              │  │                  │    │
│  │ - tables     │  │ Resources:   │  │ Resources:       │    │
│  │ - schemas    │  │ - profile    │  │ - file://        │    │
│  └──────┬───────┘  └──────┬───────┘  └─────┬────────────┘    │
│         │                 │                 │                 │
└─────────┼─────────────────┼─────────────────┼─────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │  PostgreSQL  │  │  GitHub API  │  │  Local Files     │      │
│  │  Database    │  │  (REST API)  │  │  System          │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## Communication Flow

### 1. User Query Flow

```
User types query in Gradio UI
         │
         ▼
UI Client (ui_client.py) receives input
         │
         ▼
AgentService.stream(query) is called
         │
         ▼
MCPAgent receives query + conversation history
         │
         ▼
LLM processes query and decides which tools to use
         │
         ▼
MCPClient routes tool calls to appropriate MCP servers
         │
         ▼
MCP Server executes tool (queries DB, calls GitHub API, etc.)
         │
         ▼
Result returns through the stack
         │
         ▼
LLM formats response in natural language
         │
         ▼
Streamed back to UI in real-time
         │
         ▼
User sees response in chat interface
```

### 2. Direct Tool Call Flow (No LLM)

```
Python code calls MCPManager.call_tool()
         │
         ▼
MCPClient.get_session(server).call_tool(name, args)
         │
         ▼
MCP Server executes tool
         │
         ▼
Raw result returned directly (no LLM processing)
```

## Component Responsibilities

### UI Layer (`ui_client.py`)

**Responsibilities:**
- Render web interface with Gradio
- Handle user input/output
- Display conversation history
- Show server status
- Manage UI state

**Key Methods:**
- `chat()`: Process user messages
- `get_server_status()`: Display server info
- `create_interface()`: Build Gradio UI

### Agent Layer (`agent_service.py`)

**Responsibilities:**
- Initialize and manage MCPAgent
- Configure LLM provider
- Stream responses
- Maintain conversation context
- Handle errors and retries

**Key Methods:**
- `initialize()`: Set up agent and servers
- `run()`: Execute query (blocking)
- `stream()`: Execute query (streaming)
- `cleanup()`: Close connections

### MCP Manager (`utils/mcp_manager.py`)

**Responsibilities:**
- Manage MCP client lifecycle
- Load and parse configuration
- Substitute environment variables
- Provide convenience methods
- Cache server information

**Key Methods:**
- `initialize()`: Connect to all servers
- `get_available_tools()`: List all tools
- `call_tool()`: Direct tool execution
- `get_server_status()`: Health check

### MCP Servers (Node.js)

**Responsibilities:**
- Implement MCP protocol
- Expose tools and resources
- Handle authentication (OAuth, tokens)
- Execute business logic
- Return structured results

**Protocol:**
- JSON-RPC 2.0 over stdio/HTTP/WebSocket
- Tool calls with typed parameters
- Resource reads with URIs
- Streaming support

## Data Flow Examples

### Example 1: Simple Database Query

```
User: "List all tables"
    ↓
Agent analyzes query → needs database access
    ↓
Selects postgres server → query tool
    ↓
Calls: query(sql="SELECT table_name FROM information_schema.tables")
    ↓
Postgres MCP executes SQL
    ↓
Returns: [{table_name: "users"}, {table_name: "orders"}, ...]
    ↓
LLM formats: "Your database has 3 tables: users, orders, products"
    ↓
User sees formatted response
```

### Example 2: Cross-Server Workflow

```
User: "Find developers in DB and check their GitHub repos"
    ↓
Agent plans multi-step workflow:
    ↓
Step 1: Query postgres for developers
    query(sql="SELECT github_username FROM developers")
    Returns: ["alice", "bob"]
    ↓
Step 2: For each developer, query GitHub
    list_repos(owner="alice") → [repo1, repo2]
    list_repos(owner="bob") → [repo3, repo4]
    ↓
Step 3: Aggregate and format results
    ↓
User sees: "Found 2 developers with 4 total repositories..."
```

## Configuration Management

### Environment Variables (`.env`)

```
OPENAI_API_KEY     → Used by LangChain for LLM
ANTHROPIC_API_KEY  → Alternative LLM provider
GITHUB_TOKEN       → Passed to GitHub MCP server
DATABASE_URL       → Passed to Postgres MCP server
```

### MCP Configuration (`mcp_config.json`)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",              // How to run server
      "args": ["@scope/package"],    // Server package
      "env": {                       // Environment for server
        "API_KEY": "${API_KEY}"      // Substituted from .env
      }
    }
  }
}
```

### System Prompts (`utils/prompts.py`)

```python
SYSTEM_PROMPT = """
Instructions for the AI agent on how to behave,
what to prioritize, safety guidelines, etc.
"""
```

## Conversation Memory

```
Conversation ID: "user-123-session-1"
    ↓
MCPAgent maintains history per conversation_id
    ↓
Messages stored: [
  {role: "user", content: "List tables"},
  {role: "assistant", content: "You have 3 tables..."},
  {role: "user", content: "Query the users table"},
  {role: "assistant", content: "Here are the users..."}
]
    ↓
Each new query includes full history for context
    ↓
Allows follow-up questions: "How many are there?"
(agent knows "there" refers to users)
```

## Error Handling

```
Error at any layer
    ↓
Try/except catches exception
    ↓
Agent Layer: Retry with backoff if transient
    ↓
If persistent: Format error message for user
    ↓
UI displays: "⚠️ Error: Connection to database failed"
    ↓
Logs full stack trace for debugging
    ↓
Cleanup: Close connections gracefully
```

## Security Considerations

### 1. Database Access
- Use connection pooling
- Parameterized queries only (prevent SQL injection)
- Read-only user for queries
- Rate limiting on destructive operations

### 2. GitHub API
- Token stored in environment (not code)
- Scoped tokens (minimal permissions)
- Respect rate limits
- OAuth flow for user-specific access

### 3. LLM API Keys
- Never logged or exposed
- Stored in `.env` (gitignored)
- Rotated regularly
- Usage monitoring

### 4. Agent Safety
- Confirmation required for DELETE/UPDATE/DROP
- SQL query preview before execution
- Sandbox mode available (E2B integration)
- Tool access control (disallow dangerous tools)

## Scaling Considerations

### Current Setup (Development)
- Single Python process
- Stdio connections to MCP servers
- Local database
- No load balancing

### Production Recommendations

**Horizontal Scaling:**
```
Load Balancer
    ↓
Multiple Agent Service instances
    ↓
Shared MCP servers (HTTP/WebSocket instead of stdio)
    ↓
Database connection pooling
    ↓
Redis for conversation state
```

**Optimizations:**
- Cache tool metadata
- Connection pooling for DB
- Async everywhere
- Rate limiting per user
- Circuit breakers for external APIs

## Observability

### Logging
```python
import logging

logger.info(f"Query: {query}")
logger.debug(f"Tool call: {tool_name}({args})")
logger.error(f"Error: {e}", exc_info=True)
```

### Metrics (Optional: Langfuse)
```python
from langfuse.callback import CallbackHandler

agent = MCPAgent(
    llm=llm,
    client=client,
    callbacks=[CallbackHandler()]
)

# Automatically tracks:
# - Query latency
# - Token usage
# - Tool call frequency
# - Error rates
```

### Health Checks
```python
status = service.get_server_status()
# Returns: {server: {connected: bool, tools_count: int}}

if not all(s["connected"] for s in status.values()):
    alert("MCP server down!")
```

## Extension Points

### Add New MCP Server
1. Add to `mcp_config.json`
2. Restart application
3. Tools automatically available to agent

### Add New LLM Provider
1. Install provider package
2. Update `agent_service._create_llm()`
3. Set API key in `.env`

### Customize Agent Behavior
1. Edit `utils/prompts.py`
2. Add safety rules, formatting preferences
3. Restart agent service

### Add Middleware
```python
async def logging_middleware(query, next):
    print(f"Query: {query}")
    result = await next()
    print(f"Result: {result}")
    return result

agent = MCPAgent(
    llm=llm,
    client=client,
    middleware=[logging_middleware]
)
```

## Testing Strategy

### Unit Tests
```python
# Test MCP manager
async def test_mcp_manager_init():
    manager = MCPManager("test_config.json")
    await manager.initialize()
    assert len(manager.get_available_servers()) > 0

# Test agent service
async def test_agent_query():
    service = AgentService()
    await service.initialize()
    result = await service.run("List tables")
    assert "tables" in result["response"].lower()
```

### Integration Tests
```python
# Test full stack
async def test_end_to_end():
    ui = UIClient()
    await ui.initialize()
    _, history = ui.chat("Show my repos", [])
    assert len(history) == 1
    assert history[0][1] is not None  # Has response
```

### Manual Testing
```bash
# Test MCP servers independently
npx @modelcontextprotocol/server-postgres $DATABASE_URL

# Test agent without UI
python agent_service.py

# Test full application
python run.py
```

## Deployment Architecture

### Docker Compose
```yaml
services:
  agent:
    build: .
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data

  ui:
    build: .
    command: python ui_client.py
    ports:
      - "7860:7860"
    depends_on:
      - agent
```

### Cloud Deployment
- **AWS**: ECS + RDS + ALB
- **GCP**: Cloud Run + Cloud SQL
- **Azure**: Container Instances + Postgres
- **Fly.io**: Simple deployment with Postgres addon

---

This architecture enables:
- **Modularity**: Swap components easily
- **Scalability**: Add servers/agents as needed
- **Flexibility**: Multiple LLMs, UIs, servers
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new capabilities
