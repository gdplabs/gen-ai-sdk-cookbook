"""Example of using true_positive_rate and true_negative_rate run aggregators.

This example demonstrates binary classification calibration: given a dataset where
each row is labelled TRUE (positive) or FALSE (negative), measure how well an
evaluator identifies each class.

- TRUE rows: valid responses that the evaluator should accept (aggregate_success=True)
- FALSE rows: flawed responses that the evaluator should reject (aggregate_success=False)

Run aggregators compute aggregate metrics across all evaluation results at the
end of a run (or per-suite when using evaluate_suites()).

See also:
    - Full documentation: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/run-aggregators
    - Evaluate Suites: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluate-suites
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import LLMTestCase
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

# Positive examples: correct, complete responses (label="TRUE")
POSITIVE_DATA = [
    {
        "query": "What is the capital of France?",
        "actual_output": "The capital of France is Paris.",
        "expected_output": "Paris",
        "retrieved_context": "France is a country in Europe. Paris is the capital and largest city of France.",
    },
    {
        "query": "What is 2+2?",
        "actual_output": "2+2 equals 4.",
        "expected_output": "4",
        "retrieved_context": "Basic arithmetic: 2+2 equals 4.",
    },
    {
        "query": "What is the largest planet in our solar system?",
        "actual_output": "Jupiter is the largest planet in our solar system.",
        "expected_output": "Jupiter",
        "retrieved_context": "Jupiter is the fifth planet from the Sun and the largest in the Solar System.",
    },
]

# Negative examples: incomplete or off-topic responses (label="FALSE")
NEGATIVE_DATA = [
    {
        "query": "What is the capital of France?",
        "actual_output": "France has many beautiful cities.",
        "expected_output": "Paris",
        "retrieved_context": "France is a country in Europe. Paris is the capital and largest city of France.",
    },
    {
        "query": "What is 2+2?",
        "actual_output": "Mathematics is a fascinating subject.",
        "expected_output": "4",
        "retrieved_context": "Basic arithmetic: 2+2 equals 4.",
    },
]


def _make_test_cases(rows: list[dict], label: str) -> list[LLMTestCase]:
    return [
        LLMTestCase(
            input=row["query"],
            actual_output=row["actual_output"],
            expected_output=row["expected_output"],
            retrieved_context=row["retrieved_context"],
            label=label,
        )
        for row in rows
    ]


async def main() -> None:
    """Demonstrate TPR/TNR aggregators on a binary-labelled dataset."""
    judge_model = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    data = _make_test_cases(POSITIVE_DATA, "TRUE") + _make_test_cases(NEGATIVE_DATA, "FALSE")

    result = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(
            models=[judge_model],
            metrics=[GEvalCompletenessMetric(), GEvalRedundancyMetric()],
        )],
        run_aggregators=[
            true_positive_rate,
            true_negative_rate,
        ],
        batch_size=1,
        project_name="binary_classification_demo",
    )

    print("Run Aggregators Result:")
    print(json.dumps(result.get("run_aggregators_result", {}), indent=2))

    # Expected output structure:
    # {
    #   "true_positive_rate": {
    #     "generation": 1.0    # All TRUE rows were accepted
    #   },
    #   "true_negative_rate": {
    #     "generation": 0.5    # 1 of 2 FALSE rows was rejected
    #   },
    #   "summary_accuracy": {
    #     "accuracy": 0.8      # 4 of 5 rows passed all evaluators
    #   }
    # }


if __name__ == "__main__":
    asyncio.run(main())
