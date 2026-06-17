"""Evaluate suites with binary classification (TPR/TNR) run aggregators.

Loads a dataset from CSV with a ``category`` field, dynamically builds one
EvalSuite per category, and computes TPR/TNR/accuracy run aggregators
using a CSV experiment tracker.

The CSV uses column names consistent with the library's built-in datasets
(``simple_qa_data.csv``, ``simple_rag_data.csv``) from ``gllm-evals``,
with additional ``category`` and ``label`` columns for suite grouping
and binary classification::

    question_id,category,label,query,generated_response,expected_response,retrieved_context,tools_called,expected_tools
    1,standard_rag,TRUE,"What year...","The Eiffel Tower...","1889","...",,
    6,agent_qna,TRUE,"What is 15 plus 27?","15 plus 27 equals 42.","42","...","[{...}]","[{...}]"

Each row's ``label`` (TRUE/FALSE) drives the binary classification metrics.
The ``agent_qna`` category includes tool-call data for agent evaluation.

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

from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_PATH = Path(__file__).resolve().parent / "data/eval_dataset.csv"


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
            AgentEvaluator(
                models=[judge_model],
            ),
        ],
    }

    rows = DictDataset.from_csv(path=DATA_PATH).load()

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)

    unknown = set(grouped) - set(category_evaluators)
    if unknown:
        raise ValueError(
            f"CSV contains categories not defined in category_evaluators: {unknown}. "
            f"Available: {list(category_evaluators)}"
        )

    suites = []
    for cat, cases in grouped.items():
        suite_data = []
        for row in cases:
            suite_data.append(
                LLMTestCase(
                    input=row["query"],
                    actual_output=row["generated_response"],
                    expected_output=row["expected_response"],
                    retrieved_context=row.get("retrieved_context") or None,
                    tools_called=json.loads(row["tools_called"]) if row.get("tools_called") else None,
                    expected_tools=json.loads(row["expected_tools"]) if row.get("expected_tools") else None,
                    label=row["label"],
                )
            )
        suites.append(
            EvalSuite(
                name=cat,
                data=suite_data,
                evaluators=category_evaluators[cat],
            )
        )

    result = await evaluate_suites(
        suites=suites,
        experiment_tracker=CSVExperimentTracker,
        dataset_name="binary_classification_demo",
        run_aggregators=[true_positive_rate, true_negative_rate],
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
