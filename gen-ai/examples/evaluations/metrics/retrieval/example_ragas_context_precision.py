import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.retrieval.ragas_context_precision import RagasContextPrecisionWithoutReference
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple RAGAS context precision evaluation example."""
    dataset = [
        RAGData(  # Good case (relevant context chunks are ranked higher)
            query="What is the capital of France?",
            generated_response="Paris is the capital of France.",
            retrieved_contexts=[
                "Paris is the capital and most populous city of France.",
                "It is located along the Seine River in the north-central part of the country.",
            ],
            expected_response="",
        ),
        RAGData(  # Bad case (relevant context is diluted by irrelevant ones)
            query="What is the capital of France?",
            generated_response="Paris is the capital of France.",
            retrieved_contexts=[
                "Croissants are a famous pastry in France.",
                "Many people enjoy wearing berets in France.",
                "Paris is the capital and most populous city of France.",
            ],
            expected_response="",
        ),
    ]

    # Initialize the metric using the standard SDK convention
    metric = RagasContextPrecisionWithoutReference(
        lm_model=DefaultValues.MODEL,
        lm_model_credentials=os.getenv("OPENAI_API_KEY"),
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Result:", result["ragas_context_precision_without_reference"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
