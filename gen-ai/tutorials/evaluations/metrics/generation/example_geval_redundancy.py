import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_qa_dataset
from gllm_evals.metrics.generation.geval_redundancy import (
    GEvalRedundancyMetric,
)
from gllm_evals import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_qa_dataset(data_dir)
    data = data.load()
    data = LLMTestCase(
        input=data[0].input,
        actual_output=data[0].actual_output,
    )

    # Configure the tool correctness metric
    metric = GEvalRedundancyMetric(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        ),
    )
    result = await metric.evaluate(data)
    print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
