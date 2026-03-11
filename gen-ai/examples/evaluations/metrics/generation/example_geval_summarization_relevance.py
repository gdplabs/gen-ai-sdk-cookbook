import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_summarization_relevance import GEvalSummarizationRelevanceMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Summarization Relevance evaluation example."""
    dataset = [
        RAGData(  # Good case (summary captures the main point)
            query="Summarize the meeting notes focusing on the new marketing strategy.",
            generated_response="The new marketing strategy will focus heavily on social media outreach and influencer partnerships to target younger demographics.",
            retrieved_context=[
                "The meeting discussed Q3 earnings, the new marketing strategy focusing on social media, and office renovations."
            ],
        ),
        RAGData(  # Bad case (summary misses the main point or includes irrelevant info)
            query="Summarize the meeting notes focusing on the new marketing strategy.",
            generated_response="The meeting discussed the upcoming office renovations and the budget allocated for new chairs.",
            retrieved_context=[
                "The meeting discussed Q3 earnings, the new marketing strategy focusing on social media, and office renovations."
            ],
        ),
    ]

    # Initialize the metric
    # Evaluates how well the summary captures the key information requested by the user
    metric = GEvalSummarizationRelevanceMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_summarization_relevance"]["score"])
        print("Reason:", result["geval_summarization_relevance"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
