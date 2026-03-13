import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.retrieval.deepeval_contextual_precision import DeepEvalContextualPrecisionMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple contextual precision evaluation example."""
    dataset = [
        RAGData(  # Good case (high contextual precision - relevant context is ranked first)
            query="What is the capital of France?",
            expected_response="The capital of France is Paris.",
            retrieved_context=[
                "Paris is the capital and most populous city of France.",
                "France is located in Western Europe.",
                "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
            ],
        ),
        RAGData(  # Bad case (low contextual precision - relevant context is ranked last)
            query="What is the capital of France?",
            expected_response="The capital of France is Paris.",
            retrieved_context=[
                "Croissants are a famous pastry in France.",
                "France is located in Western Europe.",
                "Paris is the capital and most populous city of France.",
            ],
        ),
    ]

    # Initialize the metric using the standard SDK convention
    metric = DeepEvalContextualPrecisionMetric(
        model=DefaultValues.MODEL, model_credentials=os.getenv("OPENAI_API_KEY"), threshold=0.5
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_contextual_precision"]["score"])
        print("Reason:", result["deepeval_contextual_precision"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
