"""
Business-Specific Evaluation Test Cases

Customize these test cases for your specific business needs.
Run with: python3.11 run_eval.py --category your_category
"""

from utils.eval_framework import EvalCase

# ============================================
# TEMPLATE: Copy and customize for your business
# ============================================

# Database Queries - Common Business Patterns
DATABASE_BUSINESS_TESTS = [
    # Sales & Revenue
    EvalCase(
        id="biz_sales_1",
        query="Show total revenue for this month",
        expected_tools=["query"],
        expected_result_contains=["revenue", "total"],
        category="sales",
        difficulty="easy"
    ),
    EvalCase(
        id="biz_sales_2",
        query="List top 10 customers by purchase amount",
        expected_tools=["query"],
        expected_result_contains=["customer", "amount"],
        category="sales",
        difficulty="medium"
    ),

    # Inventory
    EvalCase(
        id="biz_inv_1",
        query="Show products with low stock (less than 10 units)",
        expected_tools=["query"],
        expected_result_contains=["product", "stock"],
        category="inventory",
        difficulty="medium"
    ),

    # Reporting
    EvalCase(
        id="biz_report_1",
        query="Generate a summary of daily orders",
        expected_tools=["query"],
        expected_result_contains=["order", "daily"],
        category="reporting",
        difficulty="medium"
    ),

    # User/Customer Management
    EvalCase(
        id="biz_user_1",
        query="Find inactive users who haven't logged in for 30 days",
        expected_tools=["query"],
        expected_result_contains=["user", "login"],
        category="users",
        difficulty="hard"
    ),
]

# GitHub Queries - Development Workflows
GITHUB_BUSINESS_TESTS = [
    EvalCase(
        id="biz_gh_1",
        query="List all open issues assigned to me",
        expected_tools=["list_issues", "search_issues"],
        expected_result_contains=["issue"],
        category="development",
        difficulty="easy"
    ),
    EvalCase(
        id="biz_gh_2",
        query="Show recent commits to main branch",
        expected_tools=["list_commits"],
        expected_result_contains=["commit"],
        category="development",
        difficulty="easy"
    ),
    EvalCase(
        id="biz_gh_3",
        query="Find all pull requests waiting for review",
        expected_tools=["list_pull_requests"],
        expected_result_contains=["pull request", "review"],
        category="development",
        difficulty="medium"
    ),
]

# Multi-Domain Queries - Complex Business Logic
MULTI_DOMAIN_TESTS = [
    EvalCase(
        id="biz_multi_1",
        query="Show database tables and list related GitHub repos",
        expected_tools=["query", "search_repositories"],
        expected_result_contains=["table", "repo"],
        category="multi-domain",
        difficulty="hard",
        max_steps=15
    ),
    EvalCase(
        id="biz_multi_2",
        query="Find all Python files and compare with database schema",
        expected_tools=["query"],
        expected_result_contains=["python", "schema"],
        category="multi-domain",
        difficulty="hard",
        max_steps=20
    ),
]

# Compliance & Security
COMPLIANCE_TESTS = [
    EvalCase(
        id="biz_compliance_1",
        query="Show all users with admin privileges",
        expected_tools=["query"],
        expected_result_contains=["user", "admin"],
        category="compliance",
        difficulty="easy"
    ),
    EvalCase(
        id="biz_compliance_2",
        query="List all data access logs for today",
        expected_tools=["query"],
        expected_result_contains=["log", "access"],
        category="compliance",
        difficulty="medium"
    ),
]

# All business tests combined
ALL_BUSINESS_TESTS = (
    DATABASE_BUSINESS_TESTS +
    GITHUB_BUSINESS_TESTS +
    MULTI_DOMAIN_TESTS +
    COMPLIANCE_TESTS
)


def get_tests_by_category(category: str):
    """Get tests filtered by category."""
    return [t for t in ALL_BUSINESS_TESTS if t.category == category]


def get_critical_tests():
    """Get high-priority tests that must pass."""
    # Define which test IDs are critical for your business
    critical_ids = ["biz_sales_1", "biz_compliance_1", "biz_gh_1"]
    return [t for t in ALL_BUSINESS_TESTS if t.id in critical_ids]


# Usage Example:
#
# from utils.business_evals import ALL_BUSINESS_TESTS, get_critical_tests
# from utils.eval_framework import AgentEvaluator
#
# evaluator = AgentEvaluator(agent_service)
#
# # Run all business tests
# report = await evaluator.run_eval_suite(ALL_BUSINESS_TESTS)
#
# # Run only critical tests (for quick CI/CD checks)
# report = await evaluator.run_eval_suite(get_critical_tests())
