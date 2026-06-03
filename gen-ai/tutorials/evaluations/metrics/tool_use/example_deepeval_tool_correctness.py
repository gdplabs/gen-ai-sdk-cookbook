import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_agent_tool_call_dataset, load_tool_schema
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import (
    DeepEvalToolCorrectnessMetric,
)
from dotenv import load_dotenv
from gllm_evals.constant import DefaultValues
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_agent_tool_call_dataset(data_dir)

    tool_dir = Path(__file__).resolve().parent / "dataset_examples"
    available_tools = load_tool_schema(tool_dir)

    # Configure the tool correctness metric
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    tool_correctness = DeepEvalToolCorrectnessMetric(
        models=model,
        available_tools=available_tools,
    )
    result = await tool_correctness.evaluate(data[5])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
