import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.opensource.langchain_agentevals import LangChainAgentEvalsLLMAsAJudgeMetric
from gllm_evals.prompts.agentevals_prompt import TRAJECTORY_ACCURACY_CUSTOM_PROMPT
from gllm_evals.types import AgentData


async def main() -> None:
    """Run a simple LangChain AgentEvals evaluation example."""

    # 1. Initialize the metric
    # Provide the custom prompt and standard models
    metric = LangChainAgentEvalsLLMAsAJudgeMetric(
        name="my_agent_evaluator",
        prompt=TRAJECTORY_ACCURACY_CUSTOM_PROMPT,
        model=DefaultValues.MODEL,
        credentials=os.getenv("OPENAI_API_KEY"),
        continuous=False,  # Return boolean 0 or 1
        use_reasoning=True,  # Include reasoning in explanation
    )

    # 2. Define the evaluation data
    dataset = [
        AgentData(
            query="Order a large pepperoni pizza to 123 Main St.",
            agent_trajectory=[
                {"role": "user", "content": "Order a large pepperoni pizza to 123 Main St."},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "function": {
                                "name": "place_order",
                                "arguments": '{"item": "pepperoni pizza", "size": "large"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_1", "content": "Order placed."},
                {"role": "assistant", "content": "Your large pepperoni pizza has been ordered."},
            ],
            expected_agent_trajectory=[],
        )
    ]

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Result:", result["my_agent_evaluator"])
        print()


if __name__ == "__main__":
    asyncio.run(main())
