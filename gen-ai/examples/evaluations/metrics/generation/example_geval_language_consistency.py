import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_language_consistency import GEvalLanguageConsistencyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Language Consistency evaluation example."""
    dataset = [
        RAGData(  # Good case (response language matches query language)
            query="Apakah kamu bisa membantu saya?",
            generated_response="Tentu, apa yang bisa saya bantu hari ini?",
        ),
        RAGData(  # Bad case (response language differs from query language)
            query="Apakah kamu bisa membantu saya?",
            generated_response="Yes, I can totally help you with that.",
        ),
    ]

    # Initialize the metric
    metric = GEvalLanguageConsistencyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_language_consistency"]["score"])
        print("Reason:", result["geval_language_consistency"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
