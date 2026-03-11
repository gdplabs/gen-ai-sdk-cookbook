import asyncio
import os

from deepeval.test_case import ToolCallParams

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.agent.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_evals.types import AgentData


async def main() -> None:
    """Run a simple tool correctness evaluation example."""

    # Define the available tools the agent had access to
    available_tools = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_time",
            "description": "Get the current time for a location",
            "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]},
        },
    ]

    dataset = [
        AgentData(  # Good case (Called the correct tool with correct arguments)
            query="What is the weather like in Seattle right now?",
            tools_called=[{"name": "get_weather", "args": {"location": "Seattle, WA", "unit": "fahrenheit"}}],
            expected_tools=[
                {
                    "name": "get_weather",
                    "args": {"location": "Seattle, WA"},  # Only testing if it at least called the right location
                }
            ],
        ),
        AgentData(  # Bad case (Called wrong tool, or wrong arguments)
            query="What is the weather like in Seattle right now?",
            tools_called=[
                {
                    "name": "get_time",  # Wrong tool
                    "args": {"location": "Seattle, WA"},
                }
            ],
            expected_tools=[{"name": "get_weather", "args": {"location": "Seattle, WA"}}],
        ),
    ]

    # Initialize the metric
    # Note: DeepEval Tool Correctness can strict-match input parameters
    metric = DeepEvalToolCorrectnessMetric(
        model=DefaultValues.AGENT_EVALS_MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        available_tools=available_tools,
        should_exact_match=False,  # Tolerates extra correct parameters
        evaluation_params=[ToolCallParams.INPUT_PARAMETERS],  # Evaluate only based on input params
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_tool_correctness"]["score"])
        print("Reason:", result["deepeval_tool_correctness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
