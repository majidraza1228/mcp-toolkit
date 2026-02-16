Guided bug fix workflow for MCP Toolkit.

1. Ask the user to describe the bug or paste an error message.
2. Search the codebase for the relevant code using the file map:
   - `agent_service.py` - Core agent logic, streaming, LLM setup
   - `ui_client.py` - Gradio UI, chat handling
   - `utils/mcp_manager.py` - MCP connections
   - `utils/simple_memory.py` - Caching/learning
   - `utils/a2a_orchestrator.py` - Multi-agent mode
   - `utils/agentic_loop.py` - Agentic loop mode
3. Identify the root cause.
4. Apply the fix with minimal changes.
5. Verify the fix by reading the modified lines.
6. Check for the same bug pattern elsewhere (e.g., if `=` vs `+=` in one streaming path, check all 3 paths in `agent_service.py:stream()`).
7. Summarize what was fixed and why.
