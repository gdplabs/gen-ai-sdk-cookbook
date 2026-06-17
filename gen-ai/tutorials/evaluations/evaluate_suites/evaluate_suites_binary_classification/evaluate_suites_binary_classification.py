"""Evaluate suites with binary classification (TPR/TNR) run aggregators.

Loads a dataset from a local JSON file with a ``category`` field, dynamically
builds one EvalSuite per category, and computes TPR/TNR/accuracy aggregators.
"""

import asyncio
import json
import os
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv

from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"


def _to_eval_row(row: dict) -> LLMTestCase:
    return LLMTestCase(
        input=row["query"],
        actual_output=row["generated_response"],
        expected_output=row["expected_response"],
        retrieved_context=row.get("retrieved_context"),
        tools_called=row.get("tools_called"),
        expected_tools=row.get("expected_tools"),
        label=row["label"],
    )


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id=DefaultValues.MODEL,
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    category_evaluators = {
        "standard_rag": [
            GEvalGenerationEvaluator(
                metrics=[GEvalCompletenessMetric(), GEvalGroundednessMetric()],
                models=[judge_model],
            ),
        ],
        "agent_qna": [
            AgentEvaluator(models=[judge_model]),
        ],
    }

    rows = json.loads((DATA_DIR / "eval_dataset.json").read_text())

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)

    unknown = set(grouped) - set(category_evaluators)
    if unknown:
        raise ValueError(
            f"Unknown categories: {unknown}. Available: {list(category_evaluators)}"
        )

    suites = [
        EvalSuite(
            name=cat,
            data=[_to_eval_row(row) for row in cases],
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


if __name__ == "__main__":
    asyncio.run(main())
