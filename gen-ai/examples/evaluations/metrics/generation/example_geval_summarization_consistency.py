import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_summarization_consistency import GEvalSummarizationConsistencyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Summarization Consistency evaluation example."""
    dataset = [
        RAGData(  # Good case (consistent with the original text)
            query="Summarize the following: 'The cat slept on the mat all afternoon.'",
            generated_response="A cat took a nap on a mat during the afternoon.",
            retrieved_context=["The cat slept on the mat all afternoon."],
        ),
        RAGData(  # Bad case (hallucinates facts not in the original text)
            query="Summarize the following: 'The cat slept on the mat all afternoon.'",
            generated_response="A dog chased the cat off the mat.",
            retrieved_context=["The cat slept on the mat all afternoon."],
        ),
    ]

    # Initialize the metric
    # Evaluates if the summary is factually consistent with the source document
    metric = GEvalSummarizationConsistencyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_summarization_consistency"]["score"])
        print("Reason:", result["geval_summarization_consistency"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
