import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.deepeval_faithfulness import DeepEvalFaithfulnessMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple DeepEval Faithfulness evaluation example."""
    dataset = [
        RAGData(  # Good case (faithful to retrieved context)
            query="What color is the sky according to the context?",
            generated_response="The sky is blue.",
            retrieved_context=[
                "The clear daytime sky is blue because molecules in the air scatter blue light from the sun more than they scatter red light."
            ],
        ),
        RAGData(  # Bad case (hallucinated details not in context)
            query="What color is the sky according to the context?",
            generated_response="The sky is blue because of the oceans reflecting light.",
            retrieved_context=[
                "The clear daytime sky is blue because molecules in the air scatter blue light from the sun more than they scatter red light."
            ],
        ),
    ]

    # Initialize the metric
    metric = DeepEvalFaithfulnessMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        threshold=0.5,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_faithfulness"]["score"])
        print("Reason:", result["deepeval_faithfulness"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
