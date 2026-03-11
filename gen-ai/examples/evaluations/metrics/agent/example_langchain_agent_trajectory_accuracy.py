import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.agent.langchain_agent_trajectory_accuracy import LangChainAgentTrajectoryAccuracyMetric
from gllm_evals.types import AgentData


async def main() -> None:
    """Run a simple LangChain agent trajectory accuracy evaluation example."""
    dataset = [
        AgentData(  # Good case (Trajectory strictly follows expected path)
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
                                "name": "check_menu",
                                "arguments": '{"item": "pepperoni pizza", "size": "large"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_1", "content": "Available. Price: $15.99"},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_2",
                            "function": {
                                "name": "place_order",
                                "arguments": '{"item": "pepperoni pizza", "size": "large", "address": "123 Main St"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_2", "content": "Order placed successfully. ETA 30 mins."},
                {
                    "role": "assistant",
                    "content": "Your large pepperoni pizza has been ordered to 123 Main St and will arrive in 30 minutes.",
                },
            ],
            expected_agent_trajectory=[
                {"role": "user", "content": "Order a large pepperoni pizza to 123 Main St."},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "function": {
                                "name": "check_menu",
                                "arguments": '{"item": "pepperoni pizza", "size": "large"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_1", "content": "Available. Price: $15.99"},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_2",
                            "function": {
                                "name": "place_order",
                                "arguments": '{"item": "pepperoni pizza", "size": "large", "address": "123 Main St"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_2", "content": "Order placed successfully. ETA 30 mins."},
                {
                    "role": "assistant",
                    "content": "Your large pepperoni pizza has been ordered to 123 Main St and will arrive in 30 minutes.",
                },
            ],
        ),
        AgentData(  # Bad case (Agent skipped a required step or deviated)
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
                                "arguments": '{"item": "pepperoni pizza", "size": "large", "address": "123 Main St"}',
                            },
                        }
                    ],
                },  # Skipped checking menu
                {"role": "tool", "tool_call_id": "call_1", "content": "Order failed: item availability not confirmed."},
                {"role": "assistant", "content": "I couldn't place the order."},
            ],
            expected_agent_trajectory=[
                {"role": "user", "content": "Order a large pepperoni pizza to 123 Main St."},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "function": {
                                "name": "check_menu",
                                "arguments": '{"item": "pepperoni pizza", "size": "large"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_1", "content": "Available. Price: $15.99"},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_2",
                            "function": {
                                "name": "place_order",
                                "arguments": '{"item": "pepperoni pizza", "size": "large", "address": "123 Main St"}',
                            },
                        }
                    ],
                },
                {"role": "tool", "tool_call_id": "call_2", "content": "Order placed successfully. ETA 30 mins."},
                {
                    "role": "assistant",
                    "content": "Your large pepperoni pizza has been ordered to 123 Main St and will arrive in 30 minutes.",
                },
            ],
        ),
    ]

    # Initialize the metric
    # The default behavior evaluates if the actual agent_trajectory matches the expected_agent_trajectory
    metric = LangChainAgentTrajectoryAccuracyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
        continuous=False,  # Returns boolean 0 or 1
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["trajectory_accuracy"]["score"])
        print("Reason:", result["trajectory_accuracy"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
