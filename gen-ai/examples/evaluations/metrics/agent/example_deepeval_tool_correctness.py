import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_agent_tool_call_dataset, load_tool_schema
from gllm_evals.metrics.agent.deepeval_tool_correctness import (
    DeepEvalToolCorrectnessMetric,
)
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_agent_tool_call_dataset(data_dir)

    available_tools = load_tool_schema()

    # Configure the tool correctness metric
    tool_correctness = DeepEvalToolCorrectnessMetric(
        model_credentials=os.getenv("OPENAI_API_KEY"),
        available_tools=available_tools,
    )
    result = await tool_correctness.evaluate(data[5])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
