import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.retrieval.ragas_context_recall import RagasContextRecall
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple Ragas Context Recall evaluation example."""
    dataset = [
        RAGData(  # Good case (Information needed to answer expected response is perfectly recalled)
            query="What are the primary colors?",
            generated_response="The primary colors are red, blue, and yellow.",
            expected_response="Red, blue, and yellow are considered the primary colors.",
            retrieved_contexts=[
                "Primary colors are basic colors that can be mixed to produce other colors. They are red, blue, and yellow."
            ],
        ),
        RAGData(  # Bad case (Relevant snippet to answer expected response is missing from context)
            query="What are the primary colors?",
            generated_response="I cannot answer this based on the given context.",
            expected_response="Red, blue, and yellow are considered the primary colors.",
            retrieved_contexts=[
                "Colors are often categorized into warm and cool tones. Warm colors include orange and red."
            ],
        ),
    ]

    # Initialize the metric
    metric = RagasContextRecall(
        lm_model=DefaultValues.MODEL,
        lm_model_credentials=os.getenv("OPENAI_API_KEY"),
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["ragas_context_recall"]["score"])
        print("Reason:", result["ragas_context_recall"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
