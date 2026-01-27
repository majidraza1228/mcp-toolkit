"""
True Agentic Loop Implementation

Implements the Plan-Act-Observe-Reflect pattern for autonomous agent behavior.
This enables multi-step reasoning, self-correction, and goal tracking.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, AsyncIterator
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class SubGoal:
    """A sub-goal in the execution plan."""
    id: int
    description: str
    tool_hint: Optional[str] = None  # Suggested tool to use
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    attempts: int = 0


@dataclass
class ExecutionPlan:
    """Multi-step execution plan."""
    goal: str
    sub_goals: List[SubGoal] = field(default_factory=list)
    current_step: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_sub_goal(self, description: str, tool_hint: str = None):
        self.sub_goals.append(SubGoal(
            id=len(self.sub_goals),
            description=description,
            tool_hint=tool_hint
        ))

    def get_current_goal(self) -> Optional[SubGoal]:
        if self.current_step < len(self.sub_goals):
            return self.sub_goals[self.current_step]
        return None

    def advance(self):
        self.current_step += 1

    def is_complete(self) -> bool:
        return self.current_step >= len(self.sub_goals)

    def get_progress(self) -> str:
        completed = sum(1 for g in self.sub_goals if g.status == TaskStatus.COMPLETED)
        return f"{completed}/{len(self.sub_goals)}"


@dataclass
class ReflectionResult:
    """Result of agent reflection on its action."""
    success: bool
    reasoning: str
    should_retry: bool = False
    should_adjust_plan: bool = False
    new_approach: Optional[str] = None


class AgenticLoop:
    """
    Implements true agentic behavior with:
    - Planning: Break complex tasks into sub-goals
    - Acting: Execute tools toward current sub-goal
    - Observing: Check results of actions
    - Reflecting: Analyze success/failure and adjust
    """

    def __init__(
        self,
        mcp_agent: Any,
        llm: Any,
        max_iterations: int = 10,
        max_retries_per_step: int = 2
    ):
        self.mcp_agent = mcp_agent
        self.llm = llm
        self.max_iterations = max_iterations
        self.max_retries_per_step = max_retries_per_step
        self.execution_history: List[Dict] = []

    async def create_plan(self, query: str) -> ExecutionPlan:
        """Use LLM to create an execution plan for the query."""
        plan_prompt = f"""Analyze this task and break it into clear sub-goals.

Task: {query}

Return a numbered list of sub-goals. Each sub-goal should be:
1. Specific and actionable
2. Include which tool/API to use if known
3. Build on previous steps if needed

Format:
1. [Sub-goal description] (tool: tool_name_if_known)
2. [Sub-goal description] (tool: tool_name_if_known)
...

Sub-goals:"""

        try:
            response = await self.llm.ainvoke(plan_prompt)
            plan = ExecutionPlan(goal=query)

            # Parse the response into sub-goals
            lines = response.content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and line[0].isdigit():
                    # Extract description and optional tool hint
                    if '(tool:' in line.lower():
                        parts = line.split('(tool:')
                        desc = parts[0].lstrip('0123456789. ').strip()
                        tool = parts[1].rstrip(')').strip()
                        plan.add_sub_goal(desc, tool)
                    else:
                        desc = line.lstrip('0123456789. ').strip()
                        plan.add_sub_goal(desc)

            # If no sub-goals parsed, treat as single-step task
            if not plan.sub_goals:
                plan.add_sub_goal(query)

            logger.info(f"Created plan with {len(plan.sub_goals)} sub-goals")
            return plan

        except Exception as e:
            logger.error(f"Failed to create plan: {e}")
            # Fallback to single-step plan
            plan = ExecutionPlan(goal=query)
            plan.add_sub_goal(query)
            return plan

    async def execute_step(self, sub_goal: SubGoal) -> str:
        """Execute a single sub-goal and return the result."""
        sub_goal.status = TaskStatus.IN_PROGRESS
        sub_goal.attempts += 1

        # Build focused prompt for this sub-goal
        step_prompt = f"""Execute this specific task:
{sub_goal.description}

{f'Suggested tool: {sub_goal.tool_hint}' if sub_goal.tool_hint else ''}

Focus only on this task. Be concise."""

        try:
            result_chunks = []
            async for chunk in self.mcp_agent.stream(step_prompt):
                result_chunks.append(chunk)

            result = ''.join(result_chunks)
            sub_goal.result = result
            return result

        except Exception as e:
            error_msg = str(e)
            sub_goal.error = error_msg
            logger.error(f"Step execution failed: {error_msg}")
            raise

    async def reflect(self, sub_goal: SubGoal, result: str) -> ReflectionResult:
        """Reflect on the action result and decide next steps."""
        reflect_prompt = f"""Analyze if this task was completed successfully.

Task: {sub_goal.description}
Result: {result[:1000]}

Answer these questions:
1. Was the task successful? (yes/no)
2. Why or why not? (brief explanation)
3. If failed, should we retry with a different approach? (yes/no)
4. If retry, what approach should we try?

Format your response as:
SUCCESS: yes/no
REASONING: <explanation>
RETRY: yes/no
NEW_APPROACH: <approach if retry>"""

        try:
            response = await self.llm.ainvoke(reflect_prompt)
            content = response.content.strip()

            # Parse reflection response
            success = 'SUCCESS: yes' in content.lower()
            should_retry = 'RETRY: yes' in content.lower()

            reasoning = ""
            new_approach = None

            for line in content.split('\n'):
                if line.startswith('REASONING:'):
                    reasoning = line.replace('REASONING:', '').strip()
                elif line.startswith('NEW_APPROACH:'):
                    new_approach = line.replace('NEW_APPROACH:', '').strip()

            return ReflectionResult(
                success=success,
                reasoning=reasoning,
                should_retry=should_retry and not success,
                new_approach=new_approach
            )

        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            # Assume success if we can't reflect
            return ReflectionResult(success=True, reasoning="Reflection unavailable")

    async def run(self, query: str) -> AsyncIterator[str]:
        """
        Run the full agentic loop.

        Yields progress updates and final results.
        """
        # Phase 1: Planning
        yield f"🎯 **Planning**: Analyzing task...\n"
        plan = await self.create_plan(query)

        yield f"📋 **Plan created** ({len(plan.sub_goals)} steps):\n"
        for i, goal in enumerate(plan.sub_goals, 1):
            yield f"   {i}. {goal.description}\n"
        yield "\n"

        # Phase 2-5: Execute loop
        iteration = 0
        final_results = []

        while not plan.is_complete() and iteration < self.max_iterations:
            iteration += 1
            current_goal = plan.get_current_goal()

            yield f"⚡ **Step {plan.current_step + 1}/{len(plan.sub_goals)}**: {current_goal.description}\n"

            try:
                # Act
                result = await self.execute_step(current_goal)

                # Observe & Reflect
                reflection = await self.reflect(current_goal, result)

                if reflection.success:
                    current_goal.status = TaskStatus.COMPLETED
                    final_results.append(result)
                    yield f"✅ Completed: {reflection.reasoning}\n\n"
                    plan.advance()

                elif reflection.should_retry and current_goal.attempts < self.max_retries_per_step:
                    yield f"🔄 Retrying: {reflection.reasoning}\n"
                    if reflection.new_approach:
                        current_goal.description = reflection.new_approach
                        yield f"   New approach: {reflection.new_approach}\n"

                else:
                    current_goal.status = TaskStatus.FAILED
                    yield f"❌ Failed: {reflection.reasoning}\n"
                    plan.advance()  # Move on despite failure

            except Exception as e:
                yield f"⚠️ Error: {str(e)}\n"
                if current_goal.attempts >= self.max_retries_per_step:
                    current_goal.status = TaskStatus.FAILED
                    plan.advance()

            # Record history
            self.execution_history.append({
                "iteration": iteration,
                "goal": current_goal.description,
                "status": current_goal.status.value,
                "result": current_goal.result[:200] if current_goal.result else None
            })

        # Phase 6: Synthesize final response
        yield f"\n📊 **Summary** (Progress: {plan.get_progress()}):\n"
        for result in final_results:
            yield result + "\n"

        # Report any failures
        failed = [g for g in plan.sub_goals if g.status == TaskStatus.FAILED]
        if failed:
            yield f"\n⚠️ **{len(failed)} step(s) failed**:\n"
            for g in failed:
                yield f"   - {g.description}: {g.error or 'Unknown error'}\n"


class AgenticLoopFactory:
    """Factory for creating agentic loops with different configurations."""

    @staticmethod
    def create_default(mcp_agent, llm) -> AgenticLoop:
        """Create default agentic loop."""
        return AgenticLoop(
            mcp_agent=mcp_agent,
            llm=llm,
            max_iterations=10,
            max_retries_per_step=2
        )

    @staticmethod
    def create_fast(mcp_agent, llm) -> AgenticLoop:
        """Create fast agentic loop with fewer retries."""
        return AgenticLoop(
            mcp_agent=mcp_agent,
            llm=llm,
            max_iterations=5,
            max_retries_per_step=1
        )

    @staticmethod
    def create_thorough(mcp_agent, llm) -> AgenticLoop:
        """Create thorough agentic loop with more iterations."""
        return AgenticLoop(
            mcp_agent=mcp_agent,
            llm=llm,
            max_iterations=20,
            max_retries_per_step=3
        )
