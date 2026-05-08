import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from inference_mock import your_ai_func_result


async def main() -> None:
    """Run evaluation with a local CSV dataset.

    This example demonstrates the basic usage of evaluate() with:
    - Local CSV dataset loader
    - Single evaluator
    - CSV experiment tracker
    """
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in DictDataset.from_csv("dataset_examples/simple_qa_data.csv").load()
    ]
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
        experiment_tracker=CSVExperimentTracker(project_name="evals_test"),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
