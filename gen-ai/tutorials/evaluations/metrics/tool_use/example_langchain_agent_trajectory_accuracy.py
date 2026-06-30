import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_agent_dataset
from gllm_evals.metrics.tool_use.langchain_agent_trajectory_accuracy import (
    LangChainAgentTrajectoryAccuracyMetric,
)
from dotenv import load_dotenv
from gllm_evals import LLMTestCase
from gllm_evals.constant import DefaultValues
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_agent_dataset(data_dir)
    data = data.load()
    data = LLMTestCase(
        agent_trajectory=data[0].agent_trajectory,
        expected_agent_trajectory=data[0].expected_agent_trajectory,
    )

    # Configure the tool correctness metric
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    metric = LangChainAgentTrajectoryAccuracyMetric(models=model)
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
