"""
Evaluation Framework for MCP Toolkit Agent

This module provides tools to evaluate agent performance across multiple dimensions:
- Task completion accuracy
- Tool usage efficiency
- Response quality
- Error handling
- Latency and cost
"""

import json
import time
import asyncio
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class EvalCase:
    """Single evaluation test case."""
    id: str
    query: str
    expected_tools: List[str]  # Tools that should be called
    expected_result_contains: List[str]  # Keywords expected in result
    category: str  # e.g., "github", "database", "multi-domain"
    difficulty: str  # "easy", "medium", "hard"
    max_steps: int = 10  # Maximum tool calls expected
    timeout_seconds: int = 60


@dataclass
class EvalResult:
    """Result of a single evaluation."""
    case_id: str
    success: bool
    actual_tools_used: List[str]
    tool_call_count: int
    result_text: str
    latency_ms: float
    error: Optional[str] = None
    tokens_used: int = 0

    # Metrics
    tool_accuracy: float = 0.0  # % of expected tools used
    result_accuracy: float = 0.0  # % of expected keywords found
    efficiency: float = 0.0  # Expected steps / actual steps


@dataclass
class EvalReport:
    """Aggregated evaluation report."""
    timestamp: str
    total_cases: int
    passed: int
    failed: int
    pass_rate: float
    avg_latency_ms: float
    avg_tool_accuracy: float
    avg_result_accuracy: float
    avg_efficiency: float
    by_category: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    by_difficulty: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    results: List[EvalResult] = field(default_factory=list)


class AgentEvaluator:
    """Evaluates agent performance against test cases."""

    def __init__(self, agent_service):
        self.agent_service = agent_service
        self.results: List[EvalResult] = []

    async def run_single_eval(self, case: EvalCase) -> EvalResult:
        """Run a single evaluation case."""
        start_time = time.time()
        tools_used = []
        result_text = ""
        error = None

        try:
            # Collect streaming response
            async for chunk in self.agent_service.stream(case.query):
                result_text += chunk

            # Extract tools used from logs (simplified)
            # In production, instrument agent_service to track this
            tools_used = self._extract_tools_from_result(result_text)

        except asyncio.TimeoutError:
            error = f"Timeout after {case.timeout_seconds}s"
        except Exception as e:
            error = str(e)

        latency_ms = (time.time() - start_time) * 1000

        # Calculate metrics
        tool_accuracy = self._calc_tool_accuracy(case.expected_tools, tools_used)
        result_accuracy = self._calc_result_accuracy(case.expected_result_contains, result_text)
        efficiency = min(case.max_steps / max(len(tools_used), 1), 1.0)

        success = (
            error is None and
            tool_accuracy >= 0.5 and
            result_accuracy >= 0.5
        )

        return EvalResult(
            case_id=case.id,
            success=success,
            actual_tools_used=tools_used,
            tool_call_count=len(tools_used),
            result_text=result_text[:500],  # Truncate for storage
            latency_ms=latency_ms,
            error=error,
            tool_accuracy=tool_accuracy,
            result_accuracy=result_accuracy,
            efficiency=efficiency
        )

    def _extract_tools_from_result(self, result: str) -> List[str]:
        """Extract tool names from result text."""
        # This is a simplified version - in production,
        # instrument the agent to track actual tool calls
        tools = []
        tool_indicators = [
            "search_repositories", "list_issues", "query",
            "get_file_contents", "create_issue", "search_users"
        ]
        for tool in tool_indicators:
            if tool.lower() in result.lower():
                tools.append(tool)
        return tools

    def _calc_tool_accuracy(self, expected: List[str], actual: List[str]) -> float:
        """Calculate what percentage of expected tools were used."""
        if not expected:
            return 1.0
        matches = sum(1 for t in expected if t in actual)
        return matches / len(expected)

    def _calc_result_accuracy(self, expected_keywords: List[str], result: str) -> float:
        """Calculate what percentage of expected keywords are in result."""
        if not expected_keywords:
            return 1.0
        result_lower = result.lower()
        matches = sum(1 for kw in expected_keywords if kw.lower() in result_lower)
        return matches / len(expected_keywords)

    async def run_eval_suite(self, cases: List[EvalCase]) -> EvalReport:
        """Run full evaluation suite."""
        self.results = []

        for case in cases:
            logger.info(f"Running eval: {case.id}")
            result = await self.run_single_eval(case)
            self.results.append(result)

        return self._generate_report(cases)

    def _generate_report(self, cases: List[EvalCase]) -> EvalReport:
        """Generate aggregated report from results."""
        passed = sum(1 for r in self.results if r.success)

        # Group by category and difficulty
        by_category = {}
        by_difficulty = {}

        for case, result in zip(cases, self.results):
            # By category
            if case.category not in by_category:
                by_category[case.category] = {"total": 0, "passed": 0}
            by_category[case.category]["total"] += 1
            if result.success:
                by_category[case.category]["passed"] += 1

            # By difficulty
            if case.difficulty not in by_difficulty:
                by_difficulty[case.difficulty] = {"total": 0, "passed": 0}
            by_difficulty[case.difficulty]["total"] += 1
            if result.success:
                by_difficulty[case.difficulty]["passed"] += 1

        return EvalReport(
            timestamp=datetime.now().isoformat(),
            total_cases=len(self.results),
            passed=passed,
            failed=len(self.results) - passed,
            pass_rate=passed / len(self.results) if self.results else 0,
            avg_latency_ms=sum(r.latency_ms for r in self.results) / len(self.results) if self.results else 0,
            avg_tool_accuracy=sum(r.tool_accuracy for r in self.results) / len(self.results) if self.results else 0,
            avg_result_accuracy=sum(r.result_accuracy for r in self.results) / len(self.results) if self.results else 0,
            avg_efficiency=sum(r.efficiency for r in self.results) / len(self.results) if self.results else 0,
            by_category=by_category,
            by_difficulty=by_difficulty,
            results=self.results
        )

    def save_report(self, report: EvalReport, path: str = "eval_results.json"):
        """Save evaluation report to file."""
        with open(path, "w") as f:
            json.dump(asdict(report), f, indent=2)
        logger.info(f"Saved eval report to {path}")


# Pre-defined evaluation test cases
EVAL_TEST_CASES = [
    # GitHub - Easy
    EvalCase(
        id="gh_easy_1",
        query="List my GitHub repositories",
        expected_tools=["search_repositories"],
        expected_result_contains=["repository", "repo"],
        category="github",
        difficulty="easy"
    ),
    EvalCase(
        id="gh_easy_2",
        query="Search for user majidraza1228 on GitHub",
        expected_tools=["search_users"],
        expected_result_contains=["majidraza1228"],
        category="github",
        difficulty="easy"
    ),

    # GitHub - Medium
    EvalCase(
        id="gh_medium_1",
        query="Show open issues in majidraza1228/mcp-toolkit",
        expected_tools=["list_issues"],
        expected_result_contains=["issue"],
        category="github",
        difficulty="medium"
    ),

    # Database - Easy
    EvalCase(
        id="db_easy_1",
        query="List all tables in the database",
        expected_tools=["query"],
        expected_result_contains=["table"],
        category="database",
        difficulty="easy"
    ),
    EvalCase(
        id="db_easy_2",
        query="Count rows in employees table",
        expected_tools=["query"],
        expected_result_contains=["count", "employees"],
        category="database",
        difficulty="easy"
    ),

    # Database - Medium
    EvalCase(
        id="db_medium_1",
        query="Show the schema of the employees table",
        expected_tools=["query"],
        expected_result_contains=["column", "type"],
        category="database",
        difficulty="medium"
    ),

    # Multi-domain - Hard
    EvalCase(
        id="multi_hard_1",
        query="Find all GitHub repos and database tables, then summarize",
        expected_tools=["search_repositories", "query"],
        expected_result_contains=["repository", "table"],
        category="multi-domain",
        difficulty="hard",
        max_steps=15
    ),
]


async def run_quick_eval(agent_service) -> EvalReport:
    """Run a quick evaluation with pre-defined test cases."""
    evaluator = AgentEvaluator(agent_service)
    report = await evaluator.run_eval_suite(EVAL_TEST_CASES)
    evaluator.save_report(report)
    return report


def print_eval_report(report: EvalReport):
    """Print evaluation report to console."""
    print("\n" + "="*60)
    print("               AGENT EVALUATION REPORT")
    print("="*60)
    print(f"Timestamp: {report.timestamp}")
    print(f"\n📊 Overall Results:")
    print(f"   Total Cases: {report.total_cases}")
    print(f"   Passed: {report.passed} ({report.pass_rate*100:.1f}%)")
    print(f"   Failed: {report.failed}")
    print(f"\n⏱️  Performance:")
    print(f"   Avg Latency: {report.avg_latency_ms:.0f}ms")
    print(f"   Avg Efficiency: {report.avg_efficiency*100:.1f}%")
    print(f"\n🎯 Accuracy:")
    print(f"   Tool Accuracy: {report.avg_tool_accuracy*100:.1f}%")
    print(f"   Result Accuracy: {report.avg_result_accuracy*100:.1f}%")
    print(f"\n📁 By Category:")
    for cat, stats in report.by_category.items():
        rate = stats['passed']/stats['total']*100 if stats['total'] else 0
        print(f"   {cat}: {stats['passed']}/{stats['total']} ({rate:.0f}%)")
    print(f"\n📈 By Difficulty:")
    for diff, stats in report.by_difficulty.items():
        rate = stats['passed']/stats['total']*100 if stats['total'] else 0
        print(f"   {diff}: {stats['passed']}/{stats['total']} ({rate:.0f}%)")
    print("="*60 + "\n")
