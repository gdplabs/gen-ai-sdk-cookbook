import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.redundancy import RedundancyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple Redundancy evaluation example."""
    dataset = [
        RAGData(  # Good case (concise, no repetition)
            query="How does an airplane fly?",
            generated_response="Airplanes fly using lift created by the shape of their wings moving through the air.",
        ),
        RAGData(  # Bad case (contains repetitive/redundant information)
            query="How does an airplane fly?",
            generated_response="Airplanes fly because of lift. Lift is what makes them go up. The wings create lift, which allows them to fly in the air due to the lift the wings make.",
        ),
    ]

    # Initialize the metric
    metric = RedundancyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["redundancy"]["score"])
        print("Reason:", result["redundancy"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
