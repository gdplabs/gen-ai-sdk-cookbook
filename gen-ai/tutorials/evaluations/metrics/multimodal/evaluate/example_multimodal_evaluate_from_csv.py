import asyncio
import json

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from pathlib import Path


async def main() -> None:
    dataset = DictDataset.from_csv(
        str(Path(__file__).resolve().parent / "multimodal_sample_rows.csv")
    )
    suite = EvalSuite(data=dataset, evaluators=[GEvalGenerationEvaluator()])
    results = await evaluate_suites(suites=[suite], dataset_name="multimodal_evaluate_from_csv")
    print(json.dumps(results.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
