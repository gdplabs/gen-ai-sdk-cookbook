import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.deepeval_hallucination import DeepEvalHallucinationMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple DeepEval Hallucination evaluation example."""
    dataset = [
        RAGData(  # Good case (response matches context)
            query="When was the company founded?",
            generated_response="The company was founded in 2005.",
            expected_retrieved_context=["Our company was founded in 2005 by John Doe."],
            retrieved_context=["Our company was founded in 2005 by John Doe."],  # Context usually matches expected
        ),
        RAGData(  # Bad case (hallucinated founding date)
            query="When was the company founded?",
            generated_response="The company was founded in 1999.",
            expected_retrieved_context=["Our company was founded in 2005 by John Doe."],
            retrieved_context=["Our company was founded in 2005 by John Doe."],
        ),
    ]

    # Initialize the metric
    metric = DeepEvalHallucinationMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        threshold=0.5,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_hallucination"]["score"])
        print("Reason:", result["deepeval_hallucination"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
