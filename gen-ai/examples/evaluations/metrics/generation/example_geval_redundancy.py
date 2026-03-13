import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Redundancy evaluation example."""
    dataset = [
        RAGData(  # Good case (concise, no repetition)
            query="How does photosynthesis work?",
            generated_response="Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar.",
        ),
        RAGData(  # Bad case (contains repetitive/redundant information)
            query="How does photosynthesis work?",
            generated_response="Photosynthesis is the process by which plants make food. Plants use sunlight, water, and carbon dioxide to create food. This creation of food from sunlight, water, and carbon dioxide is called photosynthesis.",
        ),
    ]

    # Initialize the metric
    # Evaluates whether the generated response contains unneeded repetitive statements
    metric = GEvalRedundancyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_redundancy"]["score"])
        print("Reason:", result["geval_redundancy"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
