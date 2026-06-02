"""An example of evaluating multiple data partitions using evaluate_suites with CSV-driven test cases.

Authors:
    - Kalvin (kalvinsupriadi3@gmail.com)

References:
    [1] None
"""

import asyncio
import json
import os
from collections import defaultdict

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker
from pathlib import Path

load_dotenv()

DATA_PATH = Path(__file__).resolve().parent / "data/eval_dataset.csv"


def build_case(row: dict) -> LLMTestCase:
    return LLMTestCase(
        input=row["input"],
        actual_output=row["actual_output"],
        expected_output=row["expected_output"],
        retrieved_context=row.get("retrieved_context") or None,
    )


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    # Map suite name → evaluators.
    # Extend this when you add a new suite to the CSV.
    def _evaluators(suite_name: str):
        if suite_name == "rag":
            return [
                CompositeEvaluator(
                    metrics=[GEvalGroundednessMetric(models=[judge_model])],
                    name="groundedness",
                )
            ]
        return [GEvalGenerationEvaluator(models=[judge_model])]

    rows = DictDataset.from_csv(path=DATA_PATH).load()

    suites_by_name: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        suites_by_name[row["suite"]].append(row)

    suites = [
        EvalSuite(
            name=suite_name,
            data=[build_case(r) for r in cases],
            evaluators=_evaluators(suite_name),
        )
        for suite_name, cases in suites_by_name.items()
    ]

    result = await evaluate_suites(
        suites=suites,
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
