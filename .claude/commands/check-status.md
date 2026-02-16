Check the health and status of the MCP Toolkit application.

Run these checks and report results:

1. **Process check**: `ps aux | grep -E "(run\.py|ui_client|node)" | grep -v grep` - are the Python app and MCP servers running?
2. **Port check**: `lsof -i :7860` - is the Gradio UI listening?
3. **Config check**: Read `mcp_config.json` and verify all 3 servers (postgres, github, filesystem) are defined.
4. **Environment check**: Verify `.env` exists and contains required keys (LLM_PROVIDER, at least one API key, DATABASE_URL, GITHUB_TOKEN). Do NOT print key values.
5. **Memory check**: Read `memory_cache.json` and report cache size and hit rate.
6. **Eval check**: Read `eval_results.json` and report latest pass rate.

Summarize overall health as: HEALTHY, DEGRADED (some issues), or DOWN (not running).
