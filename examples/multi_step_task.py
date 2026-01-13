"""Multi-step task example: Complex workflow across multiple servers."""

import asyncio
from dotenv import load_dotenv

from agent_service import AgentService

load_dotenv()


async def main():
    """Execute a multi-step task across Postgres and GitHub."""
    # Initialize agent service
    service = AgentService()
    await service.initialize()

    try:
        # Multi-step workflow
        print("\n" + "="*60)
        print("Multi-Step Task: Database to GitHub Workflow")
        print("="*60 + "\n")

        tasks = [
            {
                "step": 1,
                "description": "Find all developers in database",
                "query": "Find all users in the developers table and show their GitHub usernames",
            },
            {
                "step": 2,
                "description": "Check GitHub activity",
                "query": "For the first developer found, check their recent GitHub repositories and activity",
            },
            {
                "step": 3,
                "description": "Create summary report",
                "query": "Create a summary of what you found about this developer's work",
            },
        ]

        conversation_id = "multi-step-demo"

        for task in tasks:
            print(f"\n--- Step {task['step']}: {task['description']} ---")
            print(f"Query: {task['query']}\n")

            async for chunk in service.stream(task["query"], conversation_id=conversation_id):
                if "messages" in chunk and chunk["messages"]:
                    last_message = chunk["messages"][-1]
                    if hasattr(last_message, "content"):
                        print(last_message.content, end="\r", flush=True)

            print("\n")

    finally:
        await service.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
