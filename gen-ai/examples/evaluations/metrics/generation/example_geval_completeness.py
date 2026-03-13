import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Completeness evaluation example."""
    dataset = [
        RAGData(  # Good case (answers all parts of the question)
            query="What is the capital of France and its population?",
            generated_response="The capital of France is Paris, and its population is approximately 2.1 million.",
        ),
        RAGData(  # Bad case (misses a part of the question)
            query="What is the capital of France and its population?",
            generated_response="The capital of France is Paris.",
        ),
    ]

    # Initialize the metric
    metric = GEvalCompletenessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_completeness"]["score"])
        print("Reason:", result["geval_completeness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
