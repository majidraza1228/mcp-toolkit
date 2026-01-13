"""Streaming example: Real-time agent responses."""

import asyncio
from dotenv import load_dotenv

from agent_service import AgentService

load_dotenv()


async def main():
    """Stream agent responses in real-time."""
    # Initialize agent service
    service = AgentService()
    await service.initialize()

    try:
        query = "Analyze the structure of my database and suggest optimizations"

        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60 + "\n")

        # Stream the response
        print("Agent: ", end="", flush=True)

        async for chunk in service.stream(query):
            if "messages" in chunk and chunk["messages"]:
                last_message = chunk["messages"][-1]
                if hasattr(last_message, "content"):
                    # Print incremental updates
                    print(last_message.content, end="\r", flush=True)

        print("\n")

    finally:
        await service.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
