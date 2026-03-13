import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.langchain_correctness import LangChainCorrectnessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple LangChain Correctness evaluation example."""
    dataset = [
        RAGData(  # Good case (factually correct against expected response)
            query="Who was the first president of the United States?",
            generated_response="George Washington was the first president of the United States.",
            expected_response="George Washington",
        ),
        RAGData(  # Bad case (factually incorrect)
            query="Who was the first president of the United States?",
            generated_response="Abraham Lincoln was the first president.",
            expected_response="George Washington",
        ),
    ]

    # Initialize the metric
    metric = LangChainCorrectnessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["langchain_correctness"]["score"])
        print("Reason:", result["langchain_correctness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
