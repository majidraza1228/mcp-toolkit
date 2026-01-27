# Building True Agentic Systems

![A2A Mode Interface](./screenshots/image.png)

This guide explains how to improve MCP Toolkit for true agentic behavior and how to evaluate agent performance.

## What Makes an Agent "Truly Agentic"?

| Capability | Basic Chatbot | Truly Agentic |
|------------|---------------|---------------|
| **Planning** | Single response | Multi-step plans |
| **Memory** | Session only | Long-term learning |
| **Self-correction** | None | Reflects and retries |
| **Goal tracking** | None | Tracks sub-goals |
| **Autonomy** | Waits for input | Proactive actions |

## Architecture

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

## Implementation Files

| File | Purpose |
|------|---------|
| `utils/agentic_loop.py` | Core agentic loop with Plan-Act-Observe-Reflect |
| `utils/eval_framework.py` | Evaluation framework for testing agent quality |
| `utils/a2a_orchestrator.py` | Multi-agent coordination |

## Using the Agentic Loop

```python
from utils.agentic_loop import AgenticLoop, AgenticLoopFactory

# Create agentic loop
loop = AgenticLoopFactory.create_default(mcp_agent, llm)

# Or customize
loop = AgenticLoop(
    mcp_agent=mcp_agent,
    llm=llm,
    max_iterations=15,
    max_retries_per_step=3
)

# Run with streaming output
async for chunk in loop.run("Complex multi-step query"):
    print(chunk, end="")
```

## Evaluation Framework

### Running Evaluations

```python
from utils.eval_framework import run_quick_eval, print_eval_report

# Run evaluation
report = await run_quick_eval(agent_service)

# Print results
print_eval_report(report)
```

### Creating Custom Test Cases

```python
from utils.eval_framework import EvalCase, AgentEvaluator

custom_cases = [
    EvalCase(
        id="custom_1",
        query="Your test query",
        expected_tools=["tool_1", "tool_2"],
        expected_result_contains=["keyword1", "keyword2"],
        category="your_category",
        difficulty="medium"
    ),
]

evaluator = AgentEvaluator(agent_service)
report = await evaluator.run_eval_suite(custom_cases)
```

### Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Pass Rate** | % of tests passing | > 80% |
| **Tool Accuracy** | % of expected tools used | > 70% |
| **Result Accuracy** | % of expected keywords found | > 70% |
| **Efficiency** | Expected steps / actual steps | > 60% |
| **Latency** | Average response time | < 10s |

## Improvement Roadmap

### Phase 1: Core Agentic (Current)
- [x] Multi-agent orchestration (A2A)
- [x] Basic planning
- [x] Evaluation framework
- [x] Agentic loop with reflection

### Phase 2: Advanced Memory
- [ ] Vector store for long-term memory
- [ ] Conversation summarization
- [ ] Cross-session learning
- [ ] Tool usage patterns

```python
# Future: Vector Memory
from utils.vector_memory import VectorMemory

memory = VectorMemory(embedding_model="text-embedding-3-small")
memory.store("user prefers postgres queries formatted as tables")

# Later retrieval
relevant = memory.search("how should I format database results?")
```

### Phase 3: Self-Improvement
- [ ] Automatic prompt optimization
- [ ] Tool selection learning
- [ ] Error pattern recognition
- [ ] A/B testing different strategies

### Phase 4: Advanced Autonomy
- [ ] Background task execution
- [ ] Scheduled tasks
- [ ] Proactive suggestions
- [ ] Multi-user support

## Best Practices

### 1. Evaluation-Driven Development

```bash
# Run evals before and after changes
python -c "
from utils.eval_framework import run_quick_eval
import asyncio
asyncio.run(run_quick_eval(agent_service))
"
```

### 2. Incremental Complexity

Start with simple queries, measure, then increase complexity:

```
Level 1: Single tool, single step
Level 2: Single tool, multiple steps
Level 3: Multiple tools, sequential
Level 4: Multiple tools, parallel (A2A)
Level 5: Complex reasoning with reflection
```

### 3. Monitor Key Metrics

```python
# Add to your monitoring
metrics = {
    "tool_calls_per_query": [],
    "success_rate": [],
    "avg_latency": [],
    "retry_rate": [],
}
```

### 4. Graceful Degradation

```python
# Always have fallbacks
try:
    result = await agentic_loop.run(query)
except Exception:
    # Fallback to simple mode
    result = await simple_agent.run(query)
```

## Comparing Approaches

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Simple Agent** | Fast, low cost | Limited capability | Simple queries |
| **A2A Mode** | Parallel, specialized | Higher latency | Multi-domain |
| **Agentic Loop** | Self-correcting | Slower, more tokens | Complex tasks |

## Example: Full Agentic Query

```
Query: "Find all repos with open issues, then check if any
        issues mention database problems"

PLAN (3 steps):
1. Search repositories
2. List open issues for each repo
3. Filter issues mentioning database

EXECUTE:
Step 1: ✅ Found 5 repositories
Step 2: ✅ Found 12 open issues
Step 3: ✅ 3 issues mention database

REFLECT:
- All steps completed successfully
- Found actionable results

RESULT:
Found 3 database-related issues:
- Repo A: "Database connection timeout"
- Repo B: "Query performance issue"
- Repo C: "Missing database index"
```

## Resources

- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [ReAct Pattern](https://arxiv.org/abs/2210.03629)
- [Agent Evaluation](https://www.anthropic.com/research/evaluating-ai-systems)
- [MCP Protocol](https://modelcontextprotocol.io/)
