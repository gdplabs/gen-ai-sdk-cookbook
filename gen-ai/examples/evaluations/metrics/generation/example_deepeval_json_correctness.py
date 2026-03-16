import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_qa_dataset
from gllm_evals.metrics.generation.deepeval_json_correctness import (
    DeepEvalJsonCorrectnessMetric,
)
from gllm_evals.types import QAData
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class ExampleSchema(BaseModel):
    Output: str
    Reason: str


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_qa_dataset(data_dir)
    data = data.load()
    data = QAData(
        query=data[0]["query"],
        generated_response=data[0]["generated_response"],
    )

    # Configure the tool correctness metric
    metric = DeepEvalJsonCorrectnessMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        expected_schema=ExampleSchema,
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
