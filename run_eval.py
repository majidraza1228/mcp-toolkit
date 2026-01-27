#!/usr/bin/env python3.11
"""
Run agent evaluation suite.

Usage:
    python3.11 run_eval.py              # Run all tests
    python3.11 run_eval.py --quick      # Run quick subset
    python3.11 run_eval.py --category github  # Run only GitHub tests
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent_service import AgentService
from utils.eval_framework import (
    AgentEvaluator,
    EvalCase,
    EVAL_TEST_CASES,
    print_eval_report,
)


async def run_evaluation(
    categories: list = None,
    difficulties: list = None,
    quick: bool = False,
):
    """Run evaluation suite.

    Args:
        categories: Filter by categories (github, database, multi-domain)
        difficulties: Filter by difficulties (easy, medium, hard)
        quick: Run quick subset (easy tests only)
    """
    print("🚀 Starting Agent Evaluation")
    print("=" * 60)

    # Initialize agent service
    print("\n📦 Initializing agent service...")
    service = AgentService()
    await service.initialize()

    # Filter test cases
    test_cases = EVAL_TEST_CASES.copy()

    if quick:
        test_cases = [tc for tc in test_cases if tc.difficulty == "easy"]
        print(f"⚡ Quick mode: Running {len(test_cases)} easy tests")

    if categories:
        test_cases = [tc for tc in test_cases if tc.category in categories]
        print(f"📁 Filtering by categories: {categories}")

    if difficulties:
        test_cases = [tc for tc in test_cases if tc.difficulty in difficulties]
        print(f"📈 Filtering by difficulties: {difficulties}")

    print(f"\n🧪 Running {len(test_cases)} test cases...\n")

    # Run evaluation
    evaluator = AgentEvaluator(service)
    report = await evaluator.run_eval_suite(test_cases)

    # Print report
    print_eval_report(report)

    # Save report
    evaluator.save_report(report, "eval_results.json")
    print(f"📄 Results saved to eval_results.json")

    # Cleanup
    await service.cleanup()

    # Return exit code based on pass rate
    return 0 if report.pass_rate >= 0.7 else 1


def main():
    parser = argparse.ArgumentParser(description="Run agent evaluation suite")
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Run quick evaluation (easy tests only)"
    )
    parser.add_argument(
        "--category", "-c",
        choices=["github", "database", "multi-domain"],
        action="append",
        help="Filter by category (can be used multiple times)"
    )
    parser.add_argument(
        "--difficulty", "-d",
        choices=["easy", "medium", "hard"],
        action="append",
        help="Filter by difficulty (can be used multiple times)"
    )

    args = parser.parse_args()

    exit_code = asyncio.run(run_evaluation(
        categories=args.category,
        difficulties=args.difficulty,
        quick=args.quick,
    ))

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
