import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.groundedness import GroundednessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple Groundedness evaluation example."""
    dataset = [
        RAGData(  # Good case (fully grounded in the context)
            query="What is the capital of France and what is its symbol?",
            generated_response="The capital of France is Paris and its symbol is the Eiffel Tower.",
            retrieved_context=[
                "Paris is the capital of France. The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
            ],
        ),
        RAGData(  # Bad case (hallucinated facts not in context)
            query="What is the capital of France and what is its symbol?",
            generated_response="The capital of France is Paris and its symbol is the Statue of Liberty.",
            retrieved_context=[
                "Paris is the capital of France. The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
            ],
        ),
    ]

    # Initialize the metric
    # Focuses on evaluating how grounded the generated response is based ONLY on the retrieved context (Score 1-3)
    metric = GroundednessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["groundedness"]["score"])
        print("Reason:", result["groundedness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
