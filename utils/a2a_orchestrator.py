"""A2A (Agent-to-Agent) Orchestrator for MCP Toolkit.

This module enables multiple specialized agents to collaborate on complex tasks.
Each agent specializes in a specific domain (GitHub, Database, Filesystem) and
the orchestrator routes tasks to the appropriate agent(s).
"""

import os
import asyncio
import json
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()


class AgentType(Enum):
    """Types of specialized agents."""
    GITHUB = "github"
    DATABASE = "postgres"
    FILESYSTEM = "filesystem"
    ORCHESTRATOR = "orchestrator"


@dataclass
class AgentTask:
    """A task to be executed by an agent."""
    agent_type: AgentType
    query: str
    priority: int = 1
    depends_on: Optional[List[str]] = None
    task_id: Optional[str] = None


@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent_type: AgentType
    task_id: str
    success: bool
    result: str
    error: Optional[str] = None
    execution_time: float = 0.0


# Specialized system prompts for each agent type
AGENT_PROMPTS = {
    AgentType.GITHUB: """You are a GitHub specialist agent. You excel at:
- Repository management (create, fork, clone)
- Branch operations (create, merge, delete)
- Issue and PR management
- Code search and file operations
- User and organization queries

When given a task, focus ONLY on GitHub-related operations.
Be concise and return structured data when possible.
If a task is outside your domain, respond with: "DOMAIN_MISMATCH: This task requires [domain] agent."
""",

    AgentType.DATABASE: """You are a Database specialist agent. You excel at:
- SQL query construction and optimization
- Database schema analysis
- Data retrieval and aggregation
- Table relationships and joins
- Data integrity checks

When given a task, focus ONLY on database-related operations.
Always use safe SQL practices. Never execute destructive operations without explicit confirmation.
If a task is outside your domain, respond with: "DOMAIN_MISMATCH: This task requires [domain] agent."
""",

    AgentType.FILESYSTEM: """You are a Filesystem specialist agent. You excel at:
- File and directory operations
- File content search and analysis
- Directory structure exploration
- File metadata queries
- Path manipulation

When given a task, focus ONLY on filesystem-related operations.
Be careful with file modifications and always confirm before destructive operations.
If a task is outside your domain, respond with: "DOMAIN_MISMATCH: This task requires [domain] agent."
""",

    AgentType.ORCHESTRATOR: """You are an orchestrator agent that analyzes user queries and determines:
1. Which specialized agent(s) should handle the task
2. Whether tasks can run in parallel or must be sequential
3. How to combine results from multiple agents

Analyze the query and respond with a JSON plan:
{
    "tasks": [
        {
            "agent": "github|postgres|filesystem",
            "query": "specific task for this agent",
            "priority": 1,
            "depends_on": []
        }
    ],
    "parallel": true|false,
    "reasoning": "brief explanation"
}

Available agents:
- github: GitHub operations (repos, issues, PRs, branches)
- postgres: Database queries (SQL, tables, data)
- filesystem: File operations (read, search, list)

If only one agent is needed, still return the JSON format with a single task.
"""
}


class SpecializedAgent:
    """A specialized agent for a specific domain."""

    def __init__(
        self,
        agent_type: AgentType,
        llm: Any,
        mcp_agent: Any,
    ):
        """Initialize specialized agent.

        Args:
            agent_type: Type of specialization
            llm: Language model instance
            mcp_agent: MCP agent for tool execution
        """
        self.agent_type = agent_type
        self.llm = llm
        self.mcp_agent = mcp_agent
        self.system_prompt = AGENT_PROMPTS[agent_type]

    async def execute(self, query: str) -> AgentResult:
        """Execute a task.

        Args:
            query: Task query

        Returns:
            AgentResult with execution results
        """
        import time
        start_time = time.time()
        task_id = f"{self.agent_type.value}_{int(start_time)}"

        try:
            # Add server context to query
            server_query = f"[Use only {self.agent_type.value} MCP server] {query}"

            # Execute via MCP agent
            result = await self.mcp_agent.run(server_query)

            execution_time = time.time() - start_time

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task_id,
                success=True,
                result=result,
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task_id,
                success=False,
                result="",
                error=str(e),
                execution_time=execution_time,
            )

    async def stream(self, query: str) -> AsyncIterator[str]:
        """Stream task execution.

        Args:
            query: Task query

        Yields:
            Response chunks
        """
        # Add server context to query
        server_query = f"[Use only {self.agent_type.value} MCP server] {query}"

        async for chunk in self.mcp_agent.stream(server_query):
            yield chunk


class A2AOrchestrator:
    """Orchestrator for Agent-to-Agent communication and task routing."""

    def __init__(
        self,
        mcp_agent: Any,
        available_servers: List[str],
    ):
        """Initialize the orchestrator.

        Args:
            mcp_agent: MCP agent instance
            available_servers: List of available MCP server names
        """
        self.mcp_agent = mcp_agent
        self.available_servers = available_servers
        self.llm = self._create_orchestrator_llm()
        self.agents: Dict[AgentType, SpecializedAgent] = {}
        self._initialize_agents()

    def _create_orchestrator_llm(self):
        """Create LLM for orchestration decisions."""
        llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if llm_provider == "github":
            github_token = os.getenv("GITHUB_MODELS_API_KEY") or os.getenv("GITHUB_TOKEN")
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,  # Deterministic for routing
                openai_api_key=github_token,
                openai_api_base="https://models.inference.ai.azure.com",
            )
        elif llm_provider == "anthropic":
            return ChatAnthropic(
                model=os.getenv("LLM_MODEL", "claude-sonnet-4-20250514"),
                temperature=0,
            )
        else:
            return ChatOpenAI(
                model="gpt-4o-mini",  # Use smaller model for routing
                temperature=0,
            )

    def _initialize_agents(self):
        """Initialize specialized agents for available servers."""
        server_to_agent = {
            "github": AgentType.GITHUB,
            "postgres": AgentType.DATABASE,
            "filesystem": AgentType.FILESYSTEM,
        }

        for server in self.available_servers:
            if server in server_to_agent:
                agent_type = server_to_agent[server]
                self.agents[agent_type] = SpecializedAgent(
                    agent_type=agent_type,
                    llm=self.llm,
                    mcp_agent=self.mcp_agent,
                )
                print(f"  ✓ Initialized {agent_type.value} agent")

    def _map_server_to_agent(self, server: str) -> Optional[AgentType]:
        """Map server name to agent type."""
        mapping = {
            "github": AgentType.GITHUB,
            "postgres": AgentType.DATABASE,
            "filesystem": AgentType.FILESYSTEM,
        }
        return mapping.get(server)

    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query to determine task routing.

        Args:
            query: User query

        Returns:
            Task plan with agent assignments
        """
        # If only one server available, route directly
        if len(self.available_servers) == 1:
            server = self.available_servers[0]
            return {
                "tasks": [{
                    "agent": server,
                    "query": query,
                    "priority": 1,
                    "depends_on": [],
                }],
                "parallel": False,
                "reasoning": f"Single server mode: routing to {server}",
            }

        # Use LLM to analyze and route
        messages = [
            SystemMessage(content=AGENT_PROMPTS[AgentType.ORCHESTRATOR]),
            HumanMessage(content=f"Available servers: {', '.join(self.available_servers)}\n\nUser query: {query}"),
        ]

        try:
            response = await self.llm.ainvoke(messages)
            content = response.content

            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            plan = json.loads(content.strip())

            # Validate tasks reference available servers
            valid_tasks = []
            for task in plan.get("tasks", []):
                if task.get("agent") in self.available_servers:
                    valid_tasks.append(task)

            if not valid_tasks:
                # Fallback: route to first available server
                return {
                    "tasks": [{
                        "agent": self.available_servers[0],
                        "query": query,
                        "priority": 1,
                        "depends_on": [],
                    }],
                    "parallel": False,
                    "reasoning": "Fallback routing to primary server",
                }

            plan["tasks"] = valid_tasks
            return plan

        except Exception as e:
            # Fallback on error
            print(f"  ⚠️ Orchestrator analysis failed: {e}")
            return {
                "tasks": [{
                    "agent": self.available_servers[0],
                    "query": query,
                    "priority": 1,
                    "depends_on": [],
                }],
                "parallel": False,
                "reasoning": f"Error fallback: {str(e)}",
            }

    async def execute(self, query: str) -> Dict[str, Any]:
        """Execute a query using A2A orchestration.

        Args:
            query: User query

        Returns:
            Combined results from all agents
        """
        print(f"\n🔄 A2A Orchestrator analyzing query...")

        # Analyze query to get task plan
        plan = await self.analyze_query(query)
        print(f"   Plan: {plan.get('reasoning', 'N/A')}")
        print(f"   Tasks: {len(plan['tasks'])} | Parallel: {plan.get('parallel', False)}")

        results = []

        if plan.get("parallel", False) and len(plan["tasks"]) > 1:
            # Execute tasks in parallel
            print("   ⚡ Executing tasks in parallel...")
            tasks = []
            for task_def in plan["tasks"]:
                agent_type = self._map_server_to_agent(task_def["agent"])
                if agent_type and agent_type in self.agents:
                    agent = self.agents[agent_type]
                    tasks.append(agent.execute(task_def["query"]))

            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Execute tasks sequentially
            print("   📋 Executing tasks sequentially...")
            for task_def in plan["tasks"]:
                agent_type = self._map_server_to_agent(task_def["agent"])
                if agent_type and agent_type in self.agents:
                    agent = self.agents[agent_type]
                    result = await agent.execute(task_def["query"])
                    results.append(result)

        # Combine results
        return self._combine_results(query, plan, results)

    async def stream(self, query: str) -> AsyncIterator[str]:
        """Stream execution results.

        Args:
            query: User query

        Yields:
            Response chunks
        """
        # For streaming, analyze then stream from primary agent
        plan = await self.analyze_query(query)

        yield f"🔄 **A2A Mode**: {plan.get('reasoning', 'Analyzing...')}\n\n"

        if plan["tasks"]:
            primary_task = plan["tasks"][0]
            agent_type = self._map_server_to_agent(primary_task["agent"])

            if agent_type and agent_type in self.agents:
                yield f"📍 **Agent**: {agent_type.value}\n\n"
                agent = self.agents[agent_type]
                async for chunk in agent.stream(primary_task["query"]):
                    # Handle different chunk types
                    if isinstance(chunk, str):
                        yield chunk
                    elif isinstance(chunk, tuple):
                        # Skip tuple chunks (intermediate states)
                        continue
                    elif hasattr(chunk, 'content'):
                        yield str(chunk.content)
                    else:
                        yield str(chunk)

                # If multiple tasks, execute remaining and append results
                if len(plan["tasks"]) > 1:
                    yield "\n\n---\n\n**Additional Results:**\n\n"
                    for task_def in plan["tasks"][1:]:
                        other_agent_type = self._map_server_to_agent(task_def["agent"])
                        if other_agent_type and other_agent_type in self.agents:
                            yield f"\n📍 **{other_agent_type.value}**:\n"
                            other_agent = self.agents[other_agent_type]
                            result = await other_agent.execute(task_def["query"])
                            yield result.result if result.success else f"Error: {result.error}"

    def _combine_results(
        self,
        original_query: str,
        plan: Dict[str, Any],
        results: List[AgentResult],
    ) -> Dict[str, Any]:
        """Combine results from multiple agents.

        Args:
            original_query: Original user query
            plan: Execution plan
            results: Results from agents

        Returns:
            Combined result dictionary
        """
        successful = [r for r in results if isinstance(r, AgentResult) and r.success]
        failed = [r for r in results if isinstance(r, AgentResult) and not r.success]
        exceptions = [r for r in results if isinstance(r, Exception)]

        # Build combined response
        combined_response = []

        for result in successful:
            combined_response.append(f"**{result.agent_type.value.title()} Agent** ({result.execution_time:.2f}s):\n{result.result}")

        if failed:
            for result in failed:
                combined_response.append(f"**{result.agent_type.value.title()} Agent** (failed):\n{result.error}")

        if exceptions:
            for exc in exceptions:
                combined_response.append(f"**Error**: {str(exc)}")

        return {
            "query": original_query,
            "plan": plan,
            "response": "\n\n---\n\n".join(combined_response) if combined_response else "No results",
            "agents_used": [r.agent_type.value for r in successful],
            "success": len(successful) > 0,
            "total_execution_time": sum(r.execution_time for r in successful),
        }

    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status.

        Returns:
            Status dictionary
        """
        return {
            "mode": "A2A",
            "available_agents": [a.value for a in self.agents.keys()],
            "available_servers": self.available_servers,
        }
