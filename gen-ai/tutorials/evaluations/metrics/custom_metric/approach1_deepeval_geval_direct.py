import asyncio

from deepeval.metrics.g_eval import Rubric
from deepeval.test_case import LLMTestCaseParams
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import LLMTestCase


async def main():
    data = LLMTestCase(
        input="Can you help me reset my password?",
        actual_output="Hello! Thank you for contacting us. I'd be happy to help you reset your password.",
    )

    metric = DeepEvalGEvalMetric(
        name="geval_politeness",
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
        ],
        criteria="Politeness (1-3) - Assess how polite the response is.",
        rubric=[
            Rubric(score_range=(1, 1), expected_outcome="Rude"),
            Rubric(score_range=(2, 2), expected_outcome="Neutral"),
            Rubric(score_range=(3, 3), expected_outcome="Polite"),
        ],
    )

    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
