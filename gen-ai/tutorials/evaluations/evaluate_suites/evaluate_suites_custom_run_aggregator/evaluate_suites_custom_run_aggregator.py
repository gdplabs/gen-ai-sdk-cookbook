"""Evaluate suites with a custom run aggregator.

A run aggregator receives the row-grouped evaluator results and the input rows of a run,
and returns values that evaluate_suites adds to ``run_aggregators_result``. This example
defines ``weighted_quality``, which weights low redundancy three times as much as
completeness.

References:
    [1] None
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.types import EvaluatorResult
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"


def weighted_quality(
    evaluation_results: list[list[EvaluatorResult]], data: list[LLMTestCase]
) -> dict[str, Any]:
    """Compute the average weighted quality over all rows.

    Each row holds one ``EvaluatorResult`` per evaluator, a dict that maps the evaluator name
    to an ``EvaluatorOutput``. The metric results are extra fields of that output, in
    ``model_extra``. Both metric scores are normalized to [0, 1]. Completeness is
    higher-is-better and redundancy is lower-is-better, so the row score is
    ``(completeness + 3 * (1 - redundancy)) / 4``. Rows where a metric has no score are skipped.

    Args:
        evaluation_results: Row-grouped evaluator results, parallel to ``data``.
        data: The input rows of the run.

    Returns:
        Dict with the average weighted quality.
    """
    row_scores = []
    for row_results in evaluation_results:
        generation = next(result["generation"] for result in row_results if "generation" in result)
        completeness = generation.model_extra["completeness"].score
        redundancy = generation.model_extra["redundancy"].score
        if completeness is None or redundancy is None:
            continue
        row_scores.append((completeness + 3 * (1 - redundancy)) / 4)

    return {"weighted_quality": sum(row_scores) / len(row_scores) if row_scores else 0.0}


async def main() -> None:
    dataset = DictDataset.from_csv(
        path=str(DATA_DIR / "simple_qa_data.csv"),
        field_mapping={
            "query": "input",
            "generated_response": "actual_output",
            "expected_response": "expected_output",
        },
    )
    suite = EvalSuite(
        name="qa",
        data=dataset,
        evaluators=[
            GEvalGenerationEvaluator(
                models=build_lm_invoker(
                    model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
                    credentials=os.getenv("OPENROUTER_API_KEY"),
                    config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
                ),
                metrics=[GEvalCompletenessMetric(), GEvalRedundancyMetric()],
            )
        ],
    )

    result = await evaluate_suites(
        suites=[suite],
        dataset_name="custom_run_aggregator",
        run_aggregators=[weighted_quality],
    )

    print(json.dumps(result.run_aggregators_result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
