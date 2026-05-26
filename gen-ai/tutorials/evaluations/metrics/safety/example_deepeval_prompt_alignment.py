import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_qa_dataset
from gllm_evals.metrics.generation.deepeval_prompt_alignment import (
    DeepEvalPromptAlignmentMetric,
)
from gllm_evals.constant import DefaultValues
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals import LLMTestCase
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_qa_dataset(data_dir)
    data = data.load()
    data = LLMTestCase(
        input=data[0]["query"],
        actual_output=data[0]["generated_response"],
    )

    # Configure the tool correctness metric
    metric = DeepEvalPromptAlignmentMetric(
        models=build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY")),
        prompt_instructions=["You are a helpful assistant."],
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
