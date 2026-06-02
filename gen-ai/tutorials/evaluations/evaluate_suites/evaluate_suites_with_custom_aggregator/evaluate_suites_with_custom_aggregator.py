"""An example of evaluating multiple data partitions using evaluate_suites with custom run aggregators.

Authors:
    - Kalvin (kalvinsupriadi3@gmail.com)

References:
    [1] None
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.types import EvaluatorResult, MetricInput
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


def weighted_average_score(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, float]:
    """Custom aggregator that computes weighted average score across all suites.

    This aggregator extracts every evaluator's aggregate_score across all rows
    and suites, then computes their mean. It complements the built-in
    summary_accuracy aggregator (which is always prepended automatically).

    Args:
        evaluation_results: Row-grouped evaluation outputs from all suites.
        data: List of input data for all suites.

    Returns:
        Dict containing the weighted average score.
    """
    scores = []
    for row_results in evaluation_results:
        for result in row_results:
            for eval_name, eval_data in result.items():
                if isinstance(eval_data, dict) and "aggregate_score" in eval_data:
                    scores.append(eval_data["aggregate_score"])

    if not scores:
        return {"weighted_average": 0.0}
    return {"weighted_average": sum(scores) / len(scores)}


async def main() -> None:
    """Run evaluate_suites with custom run aggregators."""
    judge_model = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    qa_suite = EvalSuite(
        name="qa",
        data=[
            LLMTestCase(
                input="What is the capital of France?",
                actual_output="Paris is the capital of France.",
                expected_output="Paris",
                retrieved_context="France is a country in Europe. Paris is the largest city.",
            ),
            LLMTestCase(
                input="What is the largest planet?",
                actual_output="Jupiter is the largest planet.",
                expected_output="Jupiter",
                retrieved_context="Jupiter is the fifth planet from the Sun.",
            ),
        ],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    rag_suite = EvalSuite(
        name="rag",
        data=[
            LLMTestCase(
                input="What year was the Eiffel Tower built?",
                actual_output="The Eiffel Tower was built in 1889.",
                expected_output="1889",
                retrieved_context="The Eiffel Tower, built for the 1889 World's Fair in Paris, is an iconic iron lattice tower.",  # noqa: E501
            ),
            LLMTestCase(
                input="Who wrote Romeo and Juliet?",
                actual_output="William Shakespeare wrote Romeo and Juliet.",
                expected_output="William Shakespeare",
                retrieved_context="Romeo and Juliet is a tragedy written by William Shakespeare early in his career.",
            ),
        ],
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            )
        ],
    )

    result = await evaluate_suites(
        suites=[qa_suite, rag_suite],
        dataset_name="custom_aggregator",
        run_aggregators=[weighted_average_score],
    )
    print(json.dumps(result.model_dump(), indent=2))

    # run_aggregators_result contains both the default accuracy
    # and the custom weighted_average metric
    print(f"\nPooled results: {json.dumps(result.run_aggregators_result, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
