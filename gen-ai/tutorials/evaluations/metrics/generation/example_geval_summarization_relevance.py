import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_summarization_dataset
from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_summarization_relevance import (
    GEvalSummarizationRelevanceMetric,
)
from gllm_evals import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_summarization_dataset(data_dir)
    data = data.load()
    data = LLMTestCase(
        input=data[0].input,
        actual_output=data[0].summary,
    )

    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))

    # Configure the tool correctness metric
    metric = GEvalSummarizationRelevanceMetric(
        models=model,
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
