import asyncio
import os

from pydantic import BaseModel

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.deepeval_json_correctness import DeepEvalJSONCorrectnessMetric
from gllm_evals.types import RAGData


class UserProfileSchema(BaseModel):
    """Pydantic schema to validate the output JSON against."""

    name: str
    age: int


async def main() -> None:
    """Run a simple DeepEval JSON Correctness evaluation example."""
    dataset = [
        RAGData(  # Good case
            query="Extract the user's name and age: 'Hi, my name is John and I am 30 years old.'",
            generated_response='{"name": "John", "age": 30}',
        ),
        RAGData(  # Bad case (missing age field)
            query="Extract the user's name and age: 'Jane is a developer.'",
            generated_response='{"name": "Jane"}',
        ),
        RAGData(  # Bad case (invalid JSON format)
            query="Extract the user's name and age.",
            generated_response="The user's name is John and age is 30.",
        ),
    ]

    # Initialize the metric with the expected Pydantic schema
    metric = DeepEvalJSONCorrectnessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        expected_schema=UserProfileSchema,
        strict_mode=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_json_correctness"]["score"])
        print("Reason:", result["deepeval_json_correctness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
