import asyncio
import json
import os
from pathlib import Path

from gllm_evals.constant import DefaultValues
from gllm_evals.dataset import load_simple_rag_dataset
from gllm_evals.metrics.retrieval.deepeval_contextual_precision import (
    DeepEvalContextualPrecisionMetric,
)
from gllm_evals import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_rag_dataset(data_dir)
    data = data.load()
    data = LLMTestCase(
        input=data[0].input,
        expected_output=data[0].expected_output,
        retrieved_context=data[0].retrieved_context,
    )

    # Configure the tool correctness metric
    metric = DeepEvalContextualPrecisionMetric(
        models=build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY")),
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
