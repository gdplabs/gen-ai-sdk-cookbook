import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"

BANKING_FEWSHOT = """
    BANKING DOMAIN EXAMPLES:
    Query: What is KYC?
    Expected: Know Your Customer - identity verification process
    Generated: KYC is identity verification
    Score: 2 (Good but missing regulatory context)
"""

BANKING_INFO = (
    "Domain: Banking and Financial Services. "
    "Penalize answers that omit regulatory context."
)


async def main() -> None:
    """Run a CSV per-row custom prompts evaluation using evaluate_suites."""
    judge_model = build_lm_invoker(
        model_id=DefaultValues.MODEL,
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    metric = GEvalCompletenessMetric(
        models=judge_model,
        fewshot=BANKING_FEWSHOT,
        additional_info=BANKING_INFO,
    )

    data = [
        LLMTestCase(**row)
        for row in DictDataset.from_csv(path=DATA_DIR / "banking_eval_data.csv").load()
    ]

    suite = EvalSuite(
        name="banking_custom_prompts",
        data=data,
        evaluators=[GEvalGenerationEvaluator(metrics=[metric])],
    )

    result = await evaluate_suites(
        suites=[suite],
        dataset_name="banking_custom_prompts",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
