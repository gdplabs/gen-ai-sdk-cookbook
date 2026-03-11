import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.deepeval_prompt_alignment import DeepEvalPromptAlignmentMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple DeepEval Prompt Alignment evaluation example."""
    dataset = [
        RAGData(  # Good case (aligns with specific instructions)
            query="Summarize the article in exactly three bullet points.",
            generated_response="- The movie was a box office success.\n- It received critical acclaim.\n- A sequel is planned for next year.",
        ),
        RAGData(  # Bad case (failed to follow specific constraints)
            query="Summarize the article in exactly three bullet points.",
            generated_response="The movie was a massive success both critically and commercially, and the director is currently planning a sequel that will begin production in the coming months.",
        ),
    ]

    # Initialize the metric
    # Validates if the generated response aligns with the rules or instructions set in the prompt
    metric = DeepEvalPromptAlignmentMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        threshold=0.5,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["deepeval_prompt_alignment"]["score"])
        print("Reason:", result["deepeval_prompt_alignment"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
