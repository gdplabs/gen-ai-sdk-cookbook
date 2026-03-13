import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.retrieval.deepeval_contextual_recall import DeepEvalContextualRecallMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple contextual recall evaluation example."""
    dataset = [
        RAGData(  # Good case (high contextual recall - retrieved context captures all facts in expected output)
            query="What are the key ingredients for making a classic Margherita pizza?",
            expected_response="A classic Margherita pizza requires San Marzano tomatoes, fresh mozzarella cheese, fresh basil, salt, and extra-virgin olive oil.",
            retrieved_context=[
                "San Marzano tomatoes, fresh mozzarella cheese, and fresh basil are essential for Margherita.",
                "Salt and extra-virgin olive oil are added as finishing touches.",
            ],
        ),
        RAGData(  # Bad case (low contextual recall - retrieved context missed most facts)
            query="What are the key ingredients for making a classic Margherita pizza?",
            expected_response="A classic Margherita pizza requires San Marzano tomatoes, fresh mozzarella cheese, fresh basil, salt, and extra-virgin olive oil.",
            retrieved_context=[
                "To make a pizza, you need dough, tomato sauce, and cheese.",
                "Baking the pizza in a wood-fired oven is traditional.",
            ],
        ),
    ]

    # Initialize the metric using the standard SDK convention
    metric = DeepEvalContextualRecallMetric(
        model=DefaultValues.MODEL, model_credentials=os.getenv("OPENAI_API_KEY"), threshold=0.5
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_contextual_recall"]["score"])
        print("Reason:", result["deepeval_contextual_recall"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
