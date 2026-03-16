import asyncio
import os

from deepeval.test_case import LLMTestCaseParams

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import RAGData


async def main():
    """Example of using DeepEvalGEvalMetric."""
    correctness_metric = DeepEvalGEvalMetric(
        name="Correctness",
        criteria="Determine whether the actual output is factually correct based on the expected output.",
        evaluation_steps=[
            "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
            "You should also heavily penalize omission of detail",
            "Vague language, or contradicting OPINIONS, are OK",
        ],
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
    )

    data = RAGData(
        query="The dog chased the cat up the tree, who ran up the tree?",
        generated_response="It depends, some might consider the cat, while others might argue the dog.",
        expected_response="The cat.",
    )

    result = await correctness_metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
