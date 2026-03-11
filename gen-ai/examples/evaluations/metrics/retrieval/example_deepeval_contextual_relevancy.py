import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.retrieval.deepeval_contextual_relevancy import DeepEvalContextualRelevancyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple contextual relevancy evaluation example."""
    dataset = [
        RAGData(  # Good case (high contextual relevancy - context chunks are highly relevant without noise)
            query="What is the capital of France?",
            generated_response="Paris is the capital of France.",
            retrieved_context=[
                "Paris is the capital and most populous city of France.",
                "It is located along the Seine River in the north-central part of the country.",
            ],
            expected_response="",
        ),
        RAGData(  # Bad case (low contextual relevancy - context contains irrelevant information noise)
            query="What is the capital of France?",
            generated_response="Paris is the capital of France.",
            retrieved_context=[
                "Paris is the capital and most populous city of France.",
                "Croissants are a famous pastry in France.",
                "Many people enjoy wearing berets in France.",
            ],
            expected_response="",
        ),
    ]

    # Initialize the metric using the standard SDK convention
    metric = DeepEvalContextualRelevancyMetric(
        model=DefaultValues.MODEL, model_credentials=os.getenv("OPENAI_API_KEY"), threshold=0.5
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_contextual_relevancy"]["score"])
        print("Reason:", result["deepeval_contextual_relevancy"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
