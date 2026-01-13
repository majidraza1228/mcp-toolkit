"""Basic example: Simple query to MCP servers."""

import asyncio
from dotenv import load_dotenv

from agent_service import AgentService

load_dotenv()


async def main():
    """Run a basic query through the agent."""
    # Initialize agent service
    service = AgentService()
    await service.initialize()

    try:
        # Simple database query
        print("\n" + "="*60)
        print("Example 1: Database Query")
        print("="*60)

        result = await service.run("List all tables in the database")
        print(f"\n{result['response']}")

        # Simple GitHub query
        print("\n" + "="*60)
        print("Example 2: GitHub Query")
        print("="*60)

        result = await service.run("Show me my GitHub repositories")
        print(f"\n{result['response']}")

    finally:
        await service.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
