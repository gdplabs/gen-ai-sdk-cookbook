import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.langchain_groundedness import LangChainGroundednessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple LangChain Groundedness evaluation example."""
    dataset = [
        RAGData(  # Good case (response matches context)
            query="When did Apollo 11 land on the moon?",
            generated_response="Apollo 11 landed on the moon on July 20, 1969.",
            retrieved_context=["On July 20, 1969, Apollo 11 became the first crewed mission to land on the Moon."],
        ),
        RAGData(  # Bad case (hallucinated fact not in context)
            query="When did Apollo 11 land on the moon?",
            generated_response="Apollo 11 landed on the moon in 1970.",
            retrieved_context=["On July 20, 1969, Apollo 11 became the first crewed mission to land on the Moon."],
        ),
    ]

    # Initialize the metric
    metric = LangChainGroundednessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["langchain_groundedness"]["score"])
        print("Reason:", result["langchain_groundedness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
