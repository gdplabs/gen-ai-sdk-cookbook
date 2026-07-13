import asyncio
import json

from gllm_evals import evaluate
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from pathlib import Path


async def main() -> None:
    dataset = DictDataset.from_csv(
        str(Path(__file__).resolve().parent / "multimodal_sample_rows.csv")
    )
    results = await evaluate(data=dataset, evaluators=[GEvalGenerationEvaluator()])
    print(json.dumps(results.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
