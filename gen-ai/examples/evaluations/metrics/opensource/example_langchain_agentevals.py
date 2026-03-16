import asyncio
import json
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.agent.langchain_agent_trajectory_accuracy import (
    LangChainAgentTrajectoryAccuracyMetric,
)
from gllm_evals.types import AgentData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Example of using LangChainAgentTrajectoryAccuracyMetric."""
    metric = LangChainAgentTrajectoryAccuracyMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
    )

    data = AgentData(
        agent_trajectory=[
            {"role": "user", "content": "What is the weather in SF?"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "get_weather",
                            "arguments": json.dumps({"city": "SF"}),
                        }
                    }
                ],
            },
            {"role": "tool", "content": "It's 80 degrees and sunny in SF."},
            {
                "role": "assistant",
                "content": "The weather in SF is 80 degrees and sunny.",
            },
        ],
        expected_agent_trajectory=[
            {"role": "user", "content": "What is the weather in SF?"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "get_weather",
                            "arguments": json.dumps({"city": "San Francisco"}),
                        }
                    }
                ],
            },
            {"role": "tool", "content": "It's 80 degrees and sunny in San Francisco."},
            {"role": "assistant", "content": "The weather in SF is 80˚ and sunny."},
        ],
    )

    result = await metric.evaluate(data)

    print(f"Input fields: {metric.get_input_fields()}")
    print(f"Required fields: {metric.required_fields}")
    print(f"Input spec: {metric.get_input_spec()}")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
