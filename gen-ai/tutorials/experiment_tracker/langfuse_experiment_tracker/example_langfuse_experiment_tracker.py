"""Example of using the Langfuse Experiment Tracker.

References:
    NONE
"""

import asyncio

from langfuse import Langfuse, get_client

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import (
    LangfuseExperimentTracker,
)
from gllm_evals.types import LLMTestCase


async def main():
    """Main function."""
    langfuse_client: Langfuse = get_client()

    data = LLMTestCase(
        question_id=1,
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris is the capital of France.",
        retrieved_context="Paris is the capital of France.",
    )

    evaluator = GEvalGenerationEvaluator()

    experiment_tracker = LangfuseExperimentTracker(
        project_name="test_langfuse_exp_tracking",
        langfuse_client=langfuse_client,
    )

    result = await evaluator.evaluate(data)

    await experiment_tracker.alog(
        dataset_name="test_langfuse_exp_tracking_dataset",
        data=data,
        evaluation_result=result,
        metadata={
            "test_metadata": "test_metadata",
            "provider": "openai",
            "model_id": "gpt-4.1",
            "method": "async",
        },
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
