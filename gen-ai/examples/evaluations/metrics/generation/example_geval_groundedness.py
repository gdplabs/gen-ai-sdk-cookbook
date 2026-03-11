import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Groundedness evaluation example."""
    dataset = [
        RAGData(  # Good case (response matches context)
            query="Who wrote the Declaration of Independence?",
            generated_response="Thomas Jefferson wrote the Declaration of Independence.",
            retrieved_context=["Thomas Jefferson is the primary author of the Declaration of Independence."],
        ),
        RAGData(  # Bad case (hallucinated fact not in context)
            query="Who wrote the Declaration of Independence?",
            generated_response="Abraham Lincoln wrote the Declaration of Independence.",
            retrieved_context=["Thomas Jefferson is the primary author of the Declaration of Independence."],
        ),
    ]

    # Initialize the metric
    metric = GEvalGroundednessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_groundedness"]["score"])
        print("Reason:", result["geval_groundedness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
