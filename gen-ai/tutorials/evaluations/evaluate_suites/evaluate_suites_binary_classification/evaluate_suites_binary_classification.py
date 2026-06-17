"""Evaluate suites with binary classification (TPR/TNR) run aggregators.

Loads a dataset from CSV with a ``category`` field, dynamically builds one
EvalSuite per category, and computes TPR/TNR/accuracy run aggregators
using a CSV experiment tracker.

The CSV uses column names consistent with the library's built-in datasets
(``simple_qa_data.csv``, ``simple_rag_data.csv``) from ``gllm-evals``,
with additional ``category`` and ``label`` columns for suite grouping
and binary classification::

    question_id,category,label,query,generated_response,expected_response,retrieved_context
    1,standard_rag,TRUE,"What year...","The Eiffel Tower...","1889","..."
    6,agent_qna,FALSE,"What is 2+2?","Mathematics is...","4","..."

Each row's ``label`` (TRUE/FALSE) drives the binary classification metrics.

Authors:
    - Kalvin (kalvinsupriadi3@gmail.com)

References:
    [1] None
"""

import asyncio
import json
import os
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_PATH = Path(__file__).resolve().parent / "data/eval_dataset.csv"


def build_case(row: dict) -> dict:
    """Map CSV columns (library convention) to evaluation input keys."""
    return {
        "input": row["query"],
        "actual_output": row["generated_response"],
        "expected_output": row["expected_response"],
        "retrieved_context": row.get("retrieved_context") or None,
        "label": row["label"],
    }


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    # Set up evaluators for each category.
    # Adding a new category CSV value + entry here creates a new suite automatically.
    category_evaluators = {
        "standard_rag": [
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            ),
            GEvalGenerationEvaluator(
                models=[judge_model],
                metrics=[GEvalCompletenessMetric()],
            ),
        ],
        "agent_qna": [
            GEvalGenerationEvaluator(
                models=[judge_model],
                metrics=[GEvalCompletenessMetric(), GEvalRedundancyMetric()],
            ),
        ],
    }

    # Load raw rows from CSV.
    # The CSV follows the same column naming convention as the library's
    # built-in datasets (simple_qa_data.csv, simple_rag_data.csv) with
    # extra columns: category, label.
    rows = DictDataset.from_csv(path=DATA_PATH).load()

    # Group rows by category
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)

    # Dynamically build one EvalSuite per category
    suites = [
        EvalSuite(
            name=cat,
            data=[build_case(r) for r in cases],
            evaluators=category_evaluators[cat],
        )
        for cat, cases in grouped.items()
    ]

    result = await evaluate_suites(
        suites=suites,
        experiment_tracker=CSVExperimentTracker,
        dataset_name="binary_classification_demo",
        run_aggregators=[true_positive_rate, true_negative_rate],
    )

    print(json.dumps(result.model_dump(), indent=2))

    # Expected output:
    # {
    #   "run_aggregators_result": {
    #     "accuracy": {                         ← auto-prepended
    #       "groundedness": 0.8,
    #       "generation": 0.6,
    #     },
    #     "true_positive_rate": {               ← only TRUE-label rows
    #       "groundedness": 1.0,
    #       "generation": 1.0,
    #     },
    #     "true_negative_rate": {               ← only FALSE-label rows
    #       "groundedness": 0.5,
    #       "generation": 1.0,
    #     },
    #   },
    #   "suites": {
    #     "standard_rag": { ... },
    #     "agent_qna": { ... },
    #   }
    # }


if __name__ == "__main__":
    asyncio.run(main())
