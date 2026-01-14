"""AI Agent service that orchestrates MCP servers using natural language."""

import os
import asyncio
from typing import Any, AsyncIterator, Dict, List, Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from mcp_use import MCPAgent

# GitHub Models (VS Code Copilot) support
try:
    from langchain_openai import AzureChatOpenAI
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from utils import MCPManager, get_system_prompt
from utils.simple_memory import SimpleMemory

# Load environment variables
load_dotenv()


class AgentService:
    """AI Agent service that uses MCP servers to perform tasks."""

    def __init__(
        self,
        config_path: str = "mcp_config.json",
        model: Optional[str] = None,
        temperature: float = 0.7,
        use_server_manager: bool = True,
    ):
        """Initialize the agent service.

        Args:
            config_path: Path to MCP configuration file
            model: LLM model to use (defaults to GPT-4)
            temperature: LLM temperature (0-1)
            use_server_manager: Whether to use server manager for auto-routing
        """
        self.config_path = config_path
        self.model = model or os.getenv("LLM_MODEL", "gpt-4")
        self.temperature = temperature
        self.use_server_manager = use_server_manager

        self.mcp_manager = MCPManager(config_path)
        self.agent: Optional[MCPAgent] = None
        self._initialized = False

        # Initialize memory system for self-learning
        self.memory = SimpleMemory()

    async def initialize(self) -> None:
        """Initialize the MCP manager and agent."""
        if self._initialized:
            return

        # Initialize MCP client connections
        await self.mcp_manager.initialize()

        # Create LLM instance
        llm = self._create_llm()

        # Create agent with MCP client
        # Set higher recursion limit to prevent getting stuck in reasoning loops
        self.agent = MCPAgent(
            llm=llm,
            client=self.mcp_manager.client,
            use_server_manager=self.use_server_manager,
            system_prompt=get_system_prompt(include_safety=True),
            max_steps=30,  # Increase from default 5 to 30
        )

        self._initialized = True
        print("✓ Agent service initialized")

    async def cleanup(self) -> None:
        """Cleanup resources."""
        await self.mcp_manager.cleanup()
        self._initialized = False

    def _create_llm(self):
        """Create LLM instance based on configuration.

        Returns:
            LangChain LLM instance
        """
        llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

        # VS Code Copilot / GitHub Models
        if llm_provider == "github" or os.getenv("GITHUB_MODELS_API_KEY"):
            github_token = os.getenv("GITHUB_MODELS_API_KEY") or os.getenv("GITHUB_TOKEN")
            if not github_token:
                raise ValueError(
                    "GitHub Models requires GITHUB_MODELS_API_KEY or GITHUB_TOKEN in .env"
                )

            # GitHub Models uses OpenAI-compatible API
            return ChatOpenAI(
                model=self.model or "gpt-4o",  # GitHub Models default
                temperature=self.temperature,
                openai_api_key=github_token,
                openai_api_base="https://models.inference.ai.azure.com",
                # Alternative endpoint: https://api.githubcopilot.com
            )

        # Standard OpenAI
        elif llm_provider == "openai" or os.getenv("OPENAI_API_KEY"):
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI requires OPENAI_API_KEY in .env")
            return ChatOpenAI(
                model=self.model or "gpt-4",
                temperature=self.temperature,
            )

        # Anthropic Claude
        elif llm_provider == "anthropic" or os.getenv("ANTHROPIC_API_KEY"):
            if not os.getenv("ANTHROPIC_API_KEY"):
                raise ValueError("Anthropic requires ANTHROPIC_API_KEY in .env")
            return ChatAnthropic(
                model=self.model or "claude-3-5-sonnet-20241022",
                temperature=self.temperature,
            )

        else:
            raise ValueError(
                "No LLM provider configured. Set LLM_PROVIDER=openai/github/anthropic "
                "and corresponding API key in .env"
            )

    async def run(self, query: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Run a query through the agent.

        Args:
            query: User's natural language query
            conversation_id: Optional conversation ID for memory

        Returns:
            Agent response with result and metadata
        """
        if not self._initialized:
            raise RuntimeError("AgentService not initialized. Call initialize() first.")

        print(f"\n🤔 Processing: {query}")

        # MCPAgent.run() doesn't accept conversation_id parameter
        # Just pass the query
        result = await self.agent.run(query)

        return {
            "query": query,
            "response": result,
            "conversation_id": conversation_id,
        }

    async def stream(
        self, query: str, conversation_id: Optional[str] = None, selected_server: str = "all"
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream agent responses in real-time.

        Args:
            query: User's natural language query
            conversation_id: Optional conversation ID for memory
            selected_server: MCP server to use ('all', 'postgres', 'github', 'filesystem')

        Yields:
            Response chunks with incremental updates
        """
        if not self._initialized:
            raise RuntimeError("AgentService not initialized. Call initialize() first.")

        # Modify query based on selected server
        if selected_server and selected_server != "all":
            query_with_context = f"[Use only {selected_server} MCP server] {query}"
        else:
            query_with_context = query

        # Check cache first for similar queries (use original query for cache key)
        cached = self.memory.get_cached_response(query)
        if cached:
            # Return cached response immediately
            yield cached["response"]
            return

        print(f"\n🤔 Processing (streaming): {query}")
        if selected_server != "all":
            print(f"   Using server: {selected_server}")

        # Collect response for caching
        full_response = ""

        try:
            # MCPAgent.stream() doesn't accept conversation_id parameter
            # Pass the query with server context if specified
            async for chunk in self.agent.stream(query_with_context):
                if isinstance(chunk, str):
                    full_response = chunk
                yield chunk

            # Save to cache if we got a response
            if full_response:
                self.memory.save_query_response(query, full_response)

        except Exception as e:
            error_message = str(e)

            # Handle recursion limit errors specifically
            if "recursion" in error_message.lower() or "GRAPH_RECURSION_LIMIT" in error_message:
                yield "⚠️ The agent encountered a complex query that required too many reasoning steps. This usually happens when:\n\n"
                yield "1. The query is ambiguous or too broad\n"
                yield "2. The required tools are not available\n"
                yield "3. The agent is trying multiple approaches\n\n"
                yield "💡 Try:\n"
                yield "- Being more specific in your query\n"
                yield "- Breaking complex requests into smaller steps\n"
                yield "- Checking that the required MCP servers are connected\n\n"
                yield f"Technical details: {error_message}"
            else:
                # Re-raise other errors
                raise

    async def get_conversation_history(
        self, conversation_id: str
    ) -> List[Dict[str, Any]]:
        """Get conversation history.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of messages in the conversation
        """
        if not self._initialized or not self.agent:
            return []

        # Access conversation memory if available
        if hasattr(self.agent, "_get_conversation_history"):
            return await self.agent._get_conversation_history(conversation_id)

        return []

    def get_available_tools(self) -> Dict[str, List[Dict]]:
        """Get all available tools from connected servers.

        Returns:
            Dictionary mapping server names to their tools
        """
        if not self._initialized:
            return {}

        return asyncio.run(self.mcp_manager.get_available_tools())

    def record_feedback(self, query: str, rating: str):
        """Record user feedback for a query.

        Args:
            query: The user's query
            rating: 'up' or 'down'
        """
        self.memory.record_feedback(query, rating)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory and learning statistics.

        Returns:
            Dictionary with memory stats
        """
        return self.memory.get_stats()

    def get_server_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all connected servers.

        Returns:
            Server status information
        """
        if not self._initialized:
            return {}

        return self.mcp_manager.get_server_status()


async def main():
    """Example usage of AgentService."""
    # Create and initialize service
    service = AgentService()
    await service.initialize()

    try:
        # Show available servers and tools
        print("\n=== Connected Servers ===")
        status = service.get_server_status()
        for server, info in status.items():
            print(f"\n{server}:")
            print(f"  Connected: {info['connected']}")
            print(f"  Tools: {', '.join(info.get('tools', []))}")

        # Example queries
        queries = [
            "List all tables in the database",
            "Show me my GitHub repositories",
            # "Find all users in the database who have a GitHub account",
        ]

        for query in queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print('='*60)

            # Stream the response
            async for chunk in service.stream(query):
                if "messages" in chunk and chunk["messages"]:
                    last_message = chunk["messages"][-1]
                    if hasattr(last_message, "content"):
                        print(last_message.content, end="", flush=True)

            print("\n")

    finally:
        # Cleanup
        await service.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
