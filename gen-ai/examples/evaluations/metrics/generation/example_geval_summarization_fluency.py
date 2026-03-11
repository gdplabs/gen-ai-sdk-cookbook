import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_summarization_fluency import GEvalSummarizationFluencyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Summarization Fluency evaluation example."""
    dataset = [
        RAGData(  # Good case (grammatically correct, fluent)
            query="Summarize the importance of exercise.",
            generated_response="Regular exercise is essential for maintaining physical and mental health. It reduces the risk of chronic diseases and improves overall well-being.",
        ),
        RAGData(  # Bad case (poor grammar, spelling errors, awkward phrasing)
            query="Summarize the importance of exercise.",
            generated_response="Exercise good for body. It make heart strong and mind happy and stop sick.",
        ),
    ]

    # Initialize the metric
    # Evaluates the grammatical correctness and natural flow of the generated text
    metric = GEvalSummarizationFluencyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_summarization_fluency"]["score"])
        print("Reason:", result["geval_summarization_fluency"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
