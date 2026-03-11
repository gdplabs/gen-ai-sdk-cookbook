import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.completeness import CompletenessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple completeness evaluation example."""
    dataset = [
        RAGData(  # Good case
            query="What are the three rules of real estate?",
            generated_response="The three rules of real estate are location, location, and location.",
        ),
        RAGData(  # Bad case
            query="What are the three rules of real estate?",
            generated_response="Location is important.",
        ),
    ]

    # Initialize the metric
    metric = CompletenessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["completeness"]["score"])
        print("Reason:", result["completeness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
