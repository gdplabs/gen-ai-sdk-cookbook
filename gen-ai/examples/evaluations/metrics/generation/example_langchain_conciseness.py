import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.langchain_conciseness import LangChainConcisenessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple LangChain Conciseness evaluation example."""
    dataset = [
        RAGData(  # Good case (concise, direct answer)
            query="What is 2 + 2?",
            generated_response="4.",
        ),
        RAGData(  # Bad case (overly verbose and unnecessary information)
            query="What is 2 + 2?",
            generated_response="When you take the number 2, which is an even prime number, and you add it to another 2, the resulting sum is exactly 4.",
        ),
    ]

    # Initialize the metric
    metric = LangChainConcisenessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["langchain_conciseness"]["score"])
        print("Reason:", result["langchain_conciseness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
