"""Evaluate suites with binary classification (TPR/TNR) run aggregators.

Loads a dataset from a local JSONL file with a ``category`` field, dynamically
builds one EvalSuite per category, and computes TPR/TNR/accuracy aggregators.

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
from gllm_evals.dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"


# Map the dataset columns to LLMTestCase fields.
FIELD_MAPPING = {
    "query": "input",
    "generated_response": "actual_output",
    "expected_response": "expected_output",
}


async def main() -> None:
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )

    category_evaluators = {
        "standard_rag": [
            GEvalGenerationEvaluator(
                models=model,
                metrics=[GEvalCompletenessMetric(), GEvalGroundednessMetric()],
            ),
        ],
        "agent_qna": [
            GEvalGenerationEvaluator(
                models=model,
                metrics=[
                    DeepEvalToolCorrectnessMetric(),
                    GEvalCompletenessMetric(),
                    GEvalGroundednessMetric(),
                    GEvalRedundancyMetric(),
                ],
            ),
        ],
    }

    rows = DictDataset.from_jsonl(str(DATA_DIR / "eval_dataset.jsonl"), field_mapping=FIELD_MAPPING).load()

    grouped: dict[str, list[LLMTestCase]] = defaultdict(list)
    for row in rows:
        grouped[row.category].append(row)

    unknown = set(grouped) - set(category_evaluators)
    if unknown:
        raise ValueError(
            f"Unknown categories: {unknown}. Available: {list(category_evaluators)}"
        )

    suites = [
        EvalSuite(
            name=cat,
            data=cases,
            evaluators=category_evaluators[cat],
        )
        for cat, cases in grouped.items()
    ]

    result = await evaluate_suites(
        suites=suites,
        dataset_name="binary_classification_demo",
        run_aggregators=[true_positive_rate, true_negative_rate],
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
