# Screenshots

## AI Agent Interface

> **Note:** To add a screenshot here, capture an image of the running application and save it as `ai-agent-interface.png` in this directory.

The interface shows the complete AI Agent with:

1. **Professional Dark Theme** - Modern, eye-friendly dark color scheme
2. **MCP Server Selector** - Dropdown to choose which server to use (postgres, github, filesystem, or all)
3. **Chat Interface** - Real-time conversation with the AI agent
4. **Feedback Buttons** - 👍 and 👎 for learning from user feedback
5. **Connected Servers Panel** - Shows available tools from each MCP server
6. **Learning Statistics** - Displays cache performance and feedback metrics
7. **Features Overview** - Lists all capabilities and connected servers

### Key Features Visible

- **Query Results**: Shows employee data retrieved from PostgreSQL database
- **Server Status**: All three MCP servers (postgres, github, filesystem) connected
- **Learning Stats**:
  - Cached Queries: 2
  - Cache Hit Rate: 0.0%
  - Positive Feedback: 1
  - Negative Feedback: 0

### How to Capture Similar Screenshot

1. Start the application: `./start.sh`
2. Open browser: http://localhost:7860
3. Ask a query like: "List all employees in the database"
4. Wait for response
5. Click 👍 or 👎 to provide feedback
6. Check the "Learning Stats" panel on the right

---

**Note:** Place the actual screenshot file `ai-agent-interface.png` in this directory for the documentation to display it correctly.
