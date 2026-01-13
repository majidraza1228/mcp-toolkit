"""Direct tool call example: Call MCP tools without LLM."""

import asyncio
from dotenv import load_dotenv

from utils import MCPManager

load_dotenv()


async def main():
    """Call MCP server tools directly without using the AI agent."""
    # Initialize MCP manager
    manager = MCPManager()
    await manager.initialize()

    try:
        # Show available servers
        print("\n=== Available Servers ===")
        servers = manager.get_available_servers()
        print(f"Connected servers: {', '.join(servers)}\n")

        # Show available tools
        print("=== Available Tools ===")
        tools = await manager.get_available_tools()
        for server, server_tools in tools.items():
            print(f"\n{server}:")
            for tool in server_tools:
                print(f"  - {tool.get('name', 'unknown')}: {tool.get('description', 'No description')}")

        # Example 1: Direct database query
        print("\n" + "="*60)
        print("Example 1: Direct Database Query (No LLM)")
        print("="*60)

        try:
            result = await manager.call_tool(
                server="postgres",
                tool="query",
                arguments={
                    "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='public' LIMIT 5"
                }
            )
            print(f"\nResult: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Example 2: Direct GitHub API call
        print("\n" + "="*60)
        print("Example 2: Direct GitHub API Call (No LLM)")
        print("="*60)

        try:
            # Note: Tool names vary by MCP server implementation
            # Check available tools for your specific GitHub server
            result = await manager.call_tool(
                server="github",
                tool="list_repositories",  # Adjust based on your server's tools
                arguments={"owner": "your-username"}  # Adjust as needed
            )
            print(f"\nResult: {result}")
        except Exception as e:
            print(f"Error: {e}")
            print("Note: Tool name may vary. Check available tools above.")

        # Example 3: Read a resource
        print("\n" + "="*60)
        print("Example 3: Read Resource")
        print("="*60)

        try:
            result = await manager.get_resource(
                server="postgres",
                uri="postgres://schema"  # Adjust based on available resources
            )
            print(f"\nResult: {result}")
        except Exception as e:
            print(f"Error: {e}")

    finally:
        await manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
