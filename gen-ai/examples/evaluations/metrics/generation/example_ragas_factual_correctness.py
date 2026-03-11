import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.ragas_factual_correctness import RagasFactualCorrectnessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple Ragas Factual Correctness evaluation example."""
    dataset = [
        RAGData(  # Good case (response matches expected references factually)
            query="Who developed the theory of relativity?",
            generated_response="Albert Einstein developed the theory of relativity.",
            expected_response="Albert Einstein",
        ),
        RAGData(  # Bad case (hallucinated fact, mismatches expected response)
            query="Who developed the theory of relativity?",
            generated_response="Isaac Newton developed the theory of relativity.",
            expected_response="Albert Einstein",
        ),
    ]

    # Initialize the metric
    metric = RagasFactualCorrectnessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["ragas_factual_correctness"]["score"])
        print("Reason:", result["ragas_factual_correctness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
