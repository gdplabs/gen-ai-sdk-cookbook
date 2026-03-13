import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.langchain_helpfulness import LangChainHelpfulnessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple LangChain Helpfulness evaluation example."""
    dataset = [
        RAGData(  # Good case (provides a direct, helpful solution)
            query="How do I reset my password?",
            generated_response="You can reset your password by clicking on the 'Forgot Password' link on the login page and following the instructions sent to your email.",
        ),
        RAGData(  # Bad case (unhelpful, evasive response)
            query="How do I reset my password?",
            generated_response="I don't know, maybe check the documentation or ask someone else.",
        ),
    ]

    # Initialize the metric
    metric = LangChainHelpfulnessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["langchain_helpfulness"]["score"])
        print("Reason:", result["langchain_helpfulness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
