# Evaluation Framework Guide

This guide covers the built-in evaluation framework for testing and measuring your MCP Toolkit agent's performance.

## Overview

The evaluation framework provides automated testing to:
- **Validate agent behavior** - Ensure tools are called correctly
- **Measure accuracy** - Track how well results match expectations
- **Monitor performance** - Measure latency and efficiency
- **Track improvements** - Compare results over time with JSON reports

## Quick Start

```bash
# Run quick evaluation (easy tests only)
python3.11 run_eval.py --quick

# Run all tests
python3.11 run_eval.py

# Filter by category
python3.11 run_eval.py --category github
python3.11 run_eval.py --category database

# Filter by difficulty
python3.11 run_eval.py --difficulty easy
python3.11 run_eval.py --difficulty hard
```

## Understanding the Metrics

### Pass Rate
Percentage of tests that complete successfully. A test passes when:
- No errors occur during execution
- Tool accuracy >= 50%
- Result accuracy >= 50%

| Pass Rate | Status |
|-----------|--------|
| > 80% | Excellent |
| 60-80% | Good |
| < 60% | Needs Improvement |

### Tool Accuracy
Measures whether the agent uses the expected tools for each query.

**How it works:**
- Compares expected tools (defined in test case) vs actual tools used
- Uses multiple detection strategies:
  1. Direct tool name mentions in response
  2. SQL/Database indicators (SELECT, FROM, table, schema)
  3. GitHub output patterns (repository, issue, commit)
  4. Filesystem patterns (directory, file content)

**Example:**
```
Expected: ["query"]
Actual: ["query"]
Tool Accuracy: 100%
```

### Result Accuracy
Measures whether the response contains expected keywords.

**Example:**
```
Expected keywords: ["table", "employees"]
Response: "The database contains tables: employees, products..."
Result Accuracy: 100% (both keywords found)
```

### Efficiency
Measures how efficiently the agent completes tasks.

```
Efficiency = Expected Steps / Actual Steps
```

- 100% = Agent used expected number of steps
- <100% = Agent used more steps than expected

### Latency
Average response time per query in milliseconds.

| Latency | Status |
|---------|--------|
| < 5s | Excellent |
| 5-10s | Good |
| > 10s | Needs Improvement |

## Sample Evaluation Report

```
============================================================
               AGENT EVALUATION REPORT
============================================================
Timestamp: 2026-01-27T00:24:40

📊 Overall Results:
   Total Cases: 4
   Passed: 3 (75.0%)
   Failed: 1

⏱️  Performance:
   Avg Latency: 9814ms
   Avg Efficiency: 100.0%

🎯 Accuracy:
   Tool Accuracy: 75.0%
   Result Accuracy: 75.0%

📁 By Category:
   github: 1/2 (50%)
   database: 2/2 (100%)

📈 By Difficulty:
   easy: 3/4 (75%)
============================================================
```

## Pre-defined Test Cases

The framework includes test cases for common scenarios:

### GitHub Tests
| ID | Query | Expected Tools | Difficulty |
|----|-------|----------------|------------|
| gh_easy_1 | List my GitHub repositories | search_repositories | easy |
| gh_easy_2 | Search for user on GitHub | search_users | easy |
| gh_medium_1 | Show open issues in repo | list_issues | medium |

### Database Tests
| ID | Query | Expected Tools | Difficulty |
|----|-------|----------------|------------|
| db_easy_1 | List all tables in database | query | easy |
| db_easy_2 | Count rows in employees table | query | easy |
| db_medium_1 | Show schema of employees table | query | medium |

### Multi-domain Tests
| ID | Query | Expected Tools | Difficulty |
|----|-------|----------------|------------|
| multi_hard_1 | Find repos and database tables | search_repositories, query | hard |

## Creating Custom Test Cases

### Basic Test Case

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

# Run evaluation
evaluator = AgentEvaluator(agent_service)
report = await evaluator.run_eval_suite(custom_cases)
```

### EvalCase Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | str | Unique identifier for the test |
| `query` | str | The natural language query to test |
| `expected_tools` | List[str] | Tools that should be called |
| `expected_result_contains` | List[str] | Keywords expected in response |
| `category` | str | Category for grouping (github, database, etc.) |
| `difficulty` | str | easy, medium, or hard |
| `max_steps` | int | Maximum expected tool calls (default: 10) |
| `timeout_seconds` | int | Timeout for the test (default: 60) |

## Business-Specific Evaluations

Create tests tailored to your business needs using `utils/business_evals.py`:

### Sales & Revenue Tests
```python
EvalCase(
    id="biz_sales_1",
    query="Show total revenue for this month",
    expected_tools=["query"],
    expected_result_contains=["revenue", "total"],
    category="sales",
    difficulty="easy"
)
```

### Compliance Tests
```python
EvalCase(
    id="biz_compliance_1",
    query="Show all users with admin privileges",
    expected_tools=["query"],
    expected_result_contains=["user", "admin"],
    category="compliance",
    difficulty="easy"
)
```

### Running Business Tests

```python
from utils.business_evals import ALL_BUSINESS_TESTS, get_critical_tests
from utils.eval_framework import AgentEvaluator

# Run all business tests
evaluator = AgentEvaluator(agent_service)
report = await evaluator.run_eval_suite(ALL_BUSINESS_TESTS)

# Run only critical tests (for CI/CD)
report = await evaluator.run_eval_suite(get_critical_tests())
```

## Business Value

### 1. Quality Assurance
- **Automated regression testing** - Catch issues before they reach users
- **Consistent benchmarking** - Track agent performance over time
- **CI/CD integration** - Run evaluations on every deployment

### 2. Performance Monitoring
- **Latency tracking** - Ensure responses are fast enough
- **Efficiency metrics** - Optimize token usage and costs
- **Error detection** - Identify failing queries early

### 3. Use Case Validation
- **Industry-specific tests** - Validate for your domain (finance, healthcare, etc.)
- **Critical path testing** - Ensure essential queries always work
- **User scenario coverage** - Test real-world usage patterns

### Example: Financial Services
```python
FINANCIAL_TESTS = [
    EvalCase(
        id="fin_audit_1",
        query="Show all transactions over $10,000 today",
        expected_tools=["query"],
        expected_result_contains=["transaction", "amount"],
        category="compliance",
        difficulty="medium"
    ),
    EvalCase(
        id="fin_report_1",
        query="Generate monthly P&L summary",
        expected_tools=["query"],
        expected_result_contains=["profit", "loss", "revenue"],
        category="reporting",
        difficulty="hard"
    ),
]
```

### Example: Healthcare
```python
HEALTHCARE_TESTS = [
    EvalCase(
        id="health_patient_1",
        query="Find patients with appointments today",
        expected_tools=["query"],
        expected_result_contains=["patient", "appointment"],
        category="scheduling",
        difficulty="easy"
    ),
]
```

## JSON Report Format

Results are saved to `eval_results.json`:

```json
{
  "timestamp": "2026-01-27T00:24:40",
  "total_cases": 4,
  "passed": 3,
  "failed": 1,
  "pass_rate": 0.75,
  "avg_latency_ms": 9813.56,
  "avg_tool_accuracy": 0.75,
  "avg_result_accuracy": 0.75,
  "avg_efficiency": 1.0,
  "by_category": {
    "github": {"total": 2, "passed": 1},
    "database": {"total": 2, "passed": 2}
  },
  "by_difficulty": {
    "easy": {"total": 4, "passed": 3}
  },
  "results": [
    {
      "case_id": "db_easy_1",
      "success": true,
      "actual_tools_used": ["query"],
      "tool_call_count": 1,
      "result_text": "The database contains tables: employees...",
      "latency_ms": 6966.53,
      "error": null,
      "tool_accuracy": 1.0,
      "result_accuracy": 1.0,
      "efficiency": 1.0
    }
  ]
}
```

## CI/CD Integration

### Exit Codes
- **0** - Pass rate >= 70%
- **1** - Pass rate < 70%

### GitHub Actions Example
```yaml
- name: Run Agent Evaluations
  run: |
    python3.11 run_eval.py --quick
    if [ $? -ne 0 ]; then
      echo "Evaluation failed - pass rate below 70%"
      exit 1
    fi
```

### Pre-deployment Checks
```bash
# Run critical tests before deployment
python3.11 -c "
import asyncio
from agent_service import AgentService
from utils.business_evals import get_critical_tests
from utils.eval_framework import AgentEvaluator

async def check():
    service = AgentService()
    await service.initialize()
    evaluator = AgentEvaluator(service)
    report = await evaluator.run_eval_suite(get_critical_tests())
    await service.cleanup()
    return report.pass_rate >= 0.9

result = asyncio.run(check())
exit(0 if result else 1)
"
```

## Troubleshooting

### Low Tool Accuracy
- Check that expected_tools match actual MCP server tool names
- Review agent logs for tool call errors
- Verify MCP servers are connected

### Low Result Accuracy
- Make expected_result_contains keywords more general
- Check that queries produce consistent outputs
- Review actual response text in eval_results.json

### High Latency
- Check LLM provider rate limits
- Consider using faster models for simple queries
- Enable caching for repeated queries

### Context Length Errors
- Reduce query complexity
- Use shorter conversation history
- Consider model with larger context window

## Related Documentation

- [Testing Guide](TESTING_GUIDE.md) - Manual testing procedures
- [Agentic Improvements](AGENTIC_IMPROVEMENTS.md) - Agentic loop patterns
- [Business Evaluations](../utils/business_evals.py) - Business test templates
