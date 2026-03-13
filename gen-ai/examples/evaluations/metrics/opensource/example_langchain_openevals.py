import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.opensource.langchain_openevals import LangChainOpenEvalsLLMAsAJudgeMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple LangChain OpenEvals evaluation example."""

    # Define a custom prompt to instruct the LLM judge
    EVALUATION_PROMPT = """You are an expert evaluator.
Evaluate whether the generated output is helpful based on the user input.
Input: {inputs}
Output: {outputs}"""

    # 1. Initialize the metric
    metric = LangChainOpenEvalsLLMAsAJudgeMetric(
        name="helpfulness_evaluator",
        prompt=EVALUATION_PROMPT,
        model=DefaultValues.MODEL,
        credentials=os.getenv("OPENAI_API_KEY"),
        continuous=True,  # Return continuous float score instead of boolean
        use_reasoning=True,
    )

    # 2. Define the evaluation data
    # OpenEvals supports tracking inputs/outputs similar to RAGData
    dataset = [
        RAGData(  # Good case
            query="How do I tie my shoes?",
            generated_response="First, make an X, then loop one lace under and pull tight. Then make two bunny ears...",
        ),
        RAGData(  # Bad case
            query="How do I tie my shoes?",
            generated_response="I don't know how to do that.",
        ),
    ]

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Result:", result["helpfulness_evaluator"])
        print()


if __name__ == "__main__":
    asyncio.run(main())
