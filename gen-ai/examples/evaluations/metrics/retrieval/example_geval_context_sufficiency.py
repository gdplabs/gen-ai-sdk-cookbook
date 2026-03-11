import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.retrieval.geval_context_sufficiency import GEvalContextSufficiencyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Context Sufficiency evaluation example."""
    dataset = [
        RAGData(  # Good case (context provides enough info to answer)
            query="How much does standard shipping cost?",
            retrieved_context=["Standard shipping costs $5.99 for all domestic orders and takes 3-5 business days."],
        ),
        RAGData(  # Bad case (context lacks necessary info to answer)
            query="How much does standard shipping cost?",
            retrieved_context=["We offer standard, expedited, and overnight shipping options for domestic orders."],
        ),
    ]

    # Initialize the metric
    # Evaluates if the context contains enough information to answer the query
    metric = GEvalContextSufficiencyMetric(
        model=DefaultValues.AGENT_EVALS_MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["context_sufficiency"]["score"])
        print("Reason:", result["context_sufficiency"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
