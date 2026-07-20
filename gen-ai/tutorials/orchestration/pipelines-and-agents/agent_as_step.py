"""Agent-as-a-Step: wrap an Agent inside a deterministic Pipeline.

This pattern embeds an AI Agent as a step in a structured pipeline, giving you
controlled execution flow with reasoning at specific stages.

Note: This script demonstrates the AgentComponent wrapper pattern without requiring
gllm-aip (the Agent package). A mock "refiner agent" replaces the real Agent
to show how the integration works. In production, replace the mock with a real
Agent from gllm-aip.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipelines-and-agents#agent-as-a-step
"""

import asyncio
from typing import TypedDict

from gllm_core.schema import main
from gllm_core.schema.component import Component
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import step, transform


# --- Mock Agent (replace with gllm_aip.Agent in production) ---

class MockAgent:
    """Simulates an Agent that refines user requests.

    In production, replace with:
        from gllm_aip import Agent
        refiner_agent = Agent(
            name="refiner",
            instruction="Rewrite the user request to be precise and unambiguous."
        )
    """

    def __init__(self, name: str, instruction: str) -> None:
        self.name = name
        self.instruction = instruction

    async def run(self, task: str) -> str:
        """Refine the task string (mock implementation)."""
        return f"[refined] {task}"


# --- AgentComponent wrapper ---

class AgentComponent(Component):
    """Wraps an Agent as a Pipeline Component."""

    def __init__(self, agent: MockAgent) -> None:
        self.agent = agent

    @main
    async def run_agent(self, task: str) -> str:
        """Run the agent and return its result."""
        return await self.agent.run(task)


# --- Pipeline using AgentComponent as a step ---

class AgentStepState(TypedDict):
    user_query: str
    refined_query: str
    final_answer: str


def generate_final_answer(data: dict) -> str:
    """Generate an answer from the refined query."""
    return f"Response based on: {data['refined_query']}"


async def main() -> None:
    """Embed an Agent as a step in a deterministic Pipeline."""

    # 1. Define an Agent (mock — replace with gllm_aip.Agent in production)
    refiner_agent = MockAgent(
        name="refiner",
        instruction="Rewrite the user request to be precise and unambiguous.",
    )

    # 2. Wrap Agent in a Component
    agent_component = AgentComponent(refiner_agent)

    # 3. Use in a Pipeline Step
    refine_step = step(
        component=agent_component,
        input_map={"task": "user_query"},
        output_state="refined_query",
    )

    # 4. Build the pipeline: refine query → generate answer
    pipeline = Pipeline(
        steps=[
            refine_step,
            transform(
                generate_final_answer,
                input_map=["refined_query"],
                output_state="final_answer",
            ),
        ],
        state_type=AgentStepState,
    )

    # 5. Execute — the pipeline runs the agent as just another step
    result = await pipeline.invoke({
        "user_query": "what is machine learning",
        "refined_query": "",
        "final_answer": "",
    })
    print(f"User query:    {result['user_query']}")
    print(f"Refined query: {result['refined_query']}")
    print(f"Final answer:  {result['final_answer']}")


if __name__ == "__main__":
    asyncio.run(main())
