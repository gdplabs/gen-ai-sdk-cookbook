import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_qa_dataset
from gllm_evals.metrics.generation.deepeval_misuse import (
    DeepEvalMisuseMetric,
)
from gllm_evals.types import QAData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_qa_dataset(data_dir)
    data = data.load()
    data = QAData(
        query=data[0]["query"],
        generated_response=data[0]["generated_response"],
    )

    # Configure the misuse metric
    metric = DeepEvalMisuseMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        domain="finance",
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
