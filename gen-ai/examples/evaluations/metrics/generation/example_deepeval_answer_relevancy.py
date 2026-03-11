import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.deepeval_answer_relevancy import DeepEvalAnswerRelevancyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple DeepEval Answer Relevancy evaluation example."""
    dataset = [
        RAGData(  # Good case
            query="What is the capital of Japan?",
            generated_response="The capital of Japan is Tokyo.",
            expected_retrieved_context=["Tokyo is the capital city of Japan."],
        ),
        RAGData(  # Bad case
            query="What is the capital of Japan?",
            generated_response="I love eating sushi and ramen.",
            expected_retrieved_context=["Tokyo is the capital city of Japan."],
        ),
    ]

    # Initialize the metric
    metric = DeepEvalAnswerRelevancyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        threshold=0.5,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_answer_relevancy"]["score"])
        print("Reason:", result["deepeval_answer_relevancy"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
