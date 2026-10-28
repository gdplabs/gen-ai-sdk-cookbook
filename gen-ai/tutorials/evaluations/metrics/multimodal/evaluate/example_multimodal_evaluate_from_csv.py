import asyncio
import json
import os

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_inference.lm_invoker import build_lm_invoker
from pathlib import Path


async def main() -> None:
    dataset = DictDataset.from_csv(
        str(Path(__file__).resolve().parent / "multimodal_sample_rows.csv")
    )
    suite = EvalSuite(
        data=dataset,
        evaluators=[
            GEvalGenerationEvaluator(
                models=build_lm_invoker(
                    model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
                    credentials=os.getenv("OPENROUTER_API_KEY"),
                    config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
                )
            )
        ],
    )
    results = await evaluate_suites(suites=[suite], dataset_name="multimodal_evaluate_from_csv")
    print(json.dumps(results.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
