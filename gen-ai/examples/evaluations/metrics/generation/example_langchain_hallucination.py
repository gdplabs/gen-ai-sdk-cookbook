import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.langchain_hallucination import LangChainHallucinationMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple LangChain Hallucination evaluation example."""
    dataset = [
        RAGData(  # Good case (no hallucination, sticks to the facts)
            query="What is the boiling point of water?",
            generated_response="The boiling point of water is 100 degrees Celsius at sea level.",
            retrieved_context=["Water boils at 100 degrees Celsius (212 degrees Fahrenheit) at sea level."],
        ),
        RAGData(  # Bad case (hallucinates an entirely fabricated fact)
            query="What is the boiling point of water?",
            generated_response="Water boils at 50 degrees Celsius on Jupiter.",
            retrieved_context=["Water boils at 100 degrees Celsius (212 degrees Fahrenheit) at sea level."],
        ),
    ]

    # Initialize the metric
    metric = LangChainHallucinationMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["langchain_hallucination"]["score"])
        print("Reason:", result["langchain_hallucination"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
