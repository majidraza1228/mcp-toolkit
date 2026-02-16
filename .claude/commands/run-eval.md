Run the MCP Toolkit evaluation suite and analyze results.

Steps:
1. Run the evaluation: `python run_eval.py`
   - For quick tests only: `python run_eval.py --quick`
   - Filter by category: `python run_eval.py --category github|database|multi-domain`
   - Filter by difficulty: `python run_eval.py --difficulty easy|medium|hard`
2. Read `eval_results.json` for the full results.
3. Summarize: pass rate, average latency, failures by category/difficulty.
4. For any failures, identify the root cause and suggest fixes.

Key metrics tracked:
- Result accuracy, safety compliance, consistency
- Pass/fail by category (github, database, multi-domain)
- Pass/fail by difficulty (easy, medium, hard)
- Average latency per query
