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
- 🔄 **A2A Mode**: Multiple specialized agents collaborate on complex tasks
- 🎯 **Agentic Loop**: Plan-Act-Observe-Reflect pattern for complex reasoning
- 📊 **Evaluation Framework**: Test and measure agent performance

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
- **[LLM Providers Guide](docs/LLM_PROVIDERS.md)** - Choose between GitHub Models (free), OpenAI, or Anthropic
- **[Architecture Overview](docs/ARCHITECTURE.md)** - Understand how it works
- **[Learning System](docs/LEARNING_SYSTEM.md)** - Self-learning capabilities explained
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Verify all features work correctly

### Advanced Topics
- **[A2A Guide](docs/A2A_GUIDE.md)** - Agent-to-Agent orchestration for multi-agent collaboration
- **[A2A vs Standard](docs/A2A_VS_STANDARD.md)** - Compare A2A and Standard modes
- **[Agentic Improvements](docs/AGENTIC_IMPROVEMENTS.md)** - True agentic patterns and evaluation framework
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Verify all features are working correctly
- **[AI Agent Explained](docs/AI_AGENT_EXPLAINED.md)** - What makes this a true AI agent
- **[Self-Learning Guide](docs/SELF_LEARNING_GUIDE.md)** - Advanced learning strategies
- **[Python Version Guide](docs/PYTHON_VERSION_GUIDE.md)** - Python version management

### Configuration
- **[mcp_config.json](mcp_config.json)** - Configure MCP servers
- **[.env.example](.env.example)** - Environment variables template

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
- Multiple LLM providers: GitHub Models (FREE), OpenAI, or Anthropic
- Automatically chooses the right tool for each task
- Provides natural language responses
- Learns from user feedback

### 🎯 Agentic Loop (NEW!)
True agentic behavior with multi-step reasoning:
- **Plan**: Breaks complex tasks into sub-goals
- **Act**: Executes tools toward current sub-goal
- **Observe**: Checks results of actions
- **Reflect**: Analyzes success/failure and adjusts
- **Self-Correction**: Retries with different approaches on failure

### 📊 Evaluation Framework (NEW!)
Built-in testing and quality measurement:
- **Pre-defined Test Cases**: GitHub, Database, Multi-domain queries
- **Metrics**: Pass rate, tool accuracy, result accuracy, efficiency
- **CLI Tool**: Run evaluations from command line
- **JSON Reports**: Save and track results over time

### 🌐 Web-Based UI
- Clean chat interface powered by Gradio
- Works in any modern browser
- No installation required for end users
- Mobile-friendly responsive design

## 🏗️ Architecture

```
Browser → Python App → AI Agent → MCP Servers → Data Sources
              │            │          ├─ PostgreSQL
              │            │          ├─ GitHub API
              │            │          └─ Filesystem
              │            │
              │            ├─ Standard Mode (single agent)
              │            ├─ A2A Mode (multi-agent orchestration)
              │            └─ Agentic Loop (plan-act-observe-reflect)
              │
              └─ Evaluation Framework (test & measure)
```

The application supports multiple agent patterns:

**Standard Mode** - Simple ReAct pattern:
1. Receives your natural language query
2. Reasons about which tools to use
3. Executes actions through MCP servers
4. Returns results in natural language

**A2A Mode** - Multi-agent orchestration:
1. Analyzes query to identify domains (GitHub, Database, Filesystem)
2. Routes to specialized agents in parallel
3. Combines results from multiple agents

**Agentic Loop** - Advanced reasoning:
1. Plans multi-step execution strategy
2. Executes each step with tool calls
3. Observes and validates results
4. Reflects on success/failure
5. Self-corrects and retries if needed

See [Architecture Overview](docs/ARCHITECTURE.md) for detailed explanation.

## 📋 Requirements

- **Python 3.11+** - Main application (required for mcp-use library)
- **Node.js** - For MCP servers
- **PostgreSQL** - Your database (optional, for database queries)
- **LLM Provider** - One of the following:
  - **GitHub Token** (FREE) - For GitHub Models with your GitHub Copilot subscription
  - **OpenAI API Key** (Paid) - For full OpenAI access
  - **Anthropic API Key** (Paid) - For Claude models

See [LLM Providers Guide](docs/LLM_PROVIDERS.md) for details.

## 🔧 Installation

1. **Clone or download this repository**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Edit `.env` file (see [LLM Providers Guide](docs/LLM_PROVIDERS.md) for details):
   ```bash
   # Choose your LLM provider (github is FREE with GitHub Copilot)
   LLM_PROVIDER=github
   LLM_MODEL=gpt-4o-mini
   GITHUB_TOKEN=your-github-token-here
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

## 🎯 Agentic Loop - Multi-Step Reasoning

The Agentic Loop enables complex, multi-step reasoning with self-correction. Unlike standard chat, it plans, executes, and reflects on each step.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC LOOP                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  PLAN    │ → │   ACT    │ → │ OBSERVE  │ → │ REFLECT  │ │
│  │          │   │          │   │          │   │          │ │
│  │ Break    │   │ Execute  │   │ Check    │   │ Analyze  │ │
│  │ into     │   │ tools    │   │ results  │   │ success  │ │
│  │ sub-goals│   │          │   │          │   │ & adjust │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       ↑                                             │       │
│       └─────────────── ITERATE ─────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Enable Agentic Mode

**Option 1: Environment Variable (always on)**
```bash
# In .env
AGENTIC_MODE=true
```

**Option 2: UI Checkbox (per-query)**
- Check the **🧠 Agentic Mode** checkbox in the UI for complex queries

### Example: Agentic Query

```
Query: "Find all repos with open issues, then summarize the database tables"

🎯 Planning: Analyzing task...
📋 Plan created (3 steps):
   1. Search repositories for the user
   2. List open issues for each repository
   3. Query database for table information

⚡ Step 1/3: Search repositories for the user
✅ Completed: Found 5 repositories

⚡ Step 2/3: List open issues for each repository
✅ Completed: Found 12 open issues

⚡ Step 3/3: Query database for table information
✅ Completed: Found 5 tables

📊 Summary (Progress: 3/3):
[Combined results from all steps...]
```

### When to Use Agentic Mode

| Query Type | Standard Mode | Agentic Mode |
|------------|---------------|--------------|
| Simple lookup | ✅ Best | Overkill |
| Multi-step task | May fail | ✅ Best |
| Cross-domain query | Limited | ✅ Best |
| Complex analysis | Unreliable | ✅ Best |

See [Agentic Improvements](docs/AGENTIC_IMPROVEMENTS.md) for more details.

## 📊 Evaluation Framework

Test and measure your agent's performance with the built-in evaluation framework.

### Run Evaluations

```bash
# Run all tests
python run_eval.py

# Quick evaluation (easy tests only)
python run_eval.py --quick

# Filter by category
python run_eval.py --category github
python run_eval.py --category database

# Filter by difficulty
python run_eval.py --difficulty easy
python run_eval.py --difficulty hard
```

### Sample Output

```
============================================================
               AGENT EVALUATION REPORT
============================================================
Timestamp: 2026-01-27T00:15:30

📊 Overall Results:
   Total Cases: 7
   Passed: 6 (85.7%)
   Failed: 1

⏱️  Performance:
   Avg Latency: 2340ms
   Avg Efficiency: 78.5%

🎯 Accuracy:
   Tool Accuracy: 82.3%
   Result Accuracy: 88.1%

📁 By Category:
   github: 2/2 (100%)
   database: 3/3 (100%)
   multi-domain: 1/2 (50%)

📈 By Difficulty:
   easy: 4/4 (100%)
   medium: 2/2 (100%)
   hard: 0/1 (0%)
============================================================
```

### Metrics Explained

| Metric | Description | Target |
|--------|-------------|--------|
| **Pass Rate** | % of tests completing successfully | > 80% |
| **Tool Accuracy** | % of expected tools used correctly | > 70% |
| **Result Accuracy** | % of expected keywords in results | > 70% |
| **Efficiency** | Expected steps / actual steps taken | > 60% |
| **Latency** | Average response time per query | < 10s |

### Custom Test Cases

```python
from utils.eval_framework import EvalCase, AgentEvaluator

custom_cases = [
    EvalCase(
        id="my_test_1",
        query="Show all employees with salary > 50000",
        expected_tools=["query"],
        expected_result_contains=["employee", "salary"],
        category="database",
        difficulty="medium"
    ),
]

evaluator = AgentEvaluator(agent_service)
report = await evaluator.run_eval_suite(custom_cases)
```

See [Agentic Improvements](docs/AGENTIC_IMPROVEMENTS.md) for complete evaluation documentation.

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

See [Architecture Overview](docs/ARCHITECTURE.md) for technical details.

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
