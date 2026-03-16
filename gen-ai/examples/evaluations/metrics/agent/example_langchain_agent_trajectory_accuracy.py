import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_agent_dataset
from gllm_evals.metrics.agent.langchain_agent_trajectory_accuracy import (
    LangChainAgentTrajectoryAccuracyMetric,
)
from dotenv import load_dotenv
from gllm_evals.types import AgentData
from gllm_evals.constant import DefaultValues

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_agent_dataset(data_dir)
    data = data.load()
    data = AgentData(
        agent_trajectory=data[0]["agent_trajectory"],
        expected_agent_trajectory=data[0]["expected_agent_trajectory"],
    )

    # Configure the tool correctness metric
    metric = LangChainAgentTrajectoryAccuracyMetric(
        model_credentials=os.getenv("OPENAI_API_KEY"),
        model=DefaultValues.AGENT_EVALS_MODEL,
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
