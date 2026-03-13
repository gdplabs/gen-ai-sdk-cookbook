import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.geval_summarization_coherence import GEvalSummarizationCoherenceMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple GEval Summarization Coherence evaluation example."""
    dataset = [
        RAGData(  # Good case (reads smoothly and logically)
            query="Summarize the importance of bees.",
            generated_response="Bees are crucial for pollinating a wide variety of plants. Without them, global agriculture would suffer significantly.",
        ),
        RAGData(  # Bad case (disjointed, abrupt transitions, poor logic)
            query="Summarize the importance of bees.",
            generated_response="Bees fly around. Agriculture is big. Honey tastes sweet but plants need pollen so bees are important.",
        ),
    ]

    # Initialize the metric
    # Evaluates the structural and logical coherence of a generated summary
    metric = GEvalSummarizationCoherenceMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["geval_summarization_coherence"]["score"])
        print("Reason:", result["geval_summarization_coherence"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
