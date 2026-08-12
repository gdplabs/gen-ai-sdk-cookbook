import asyncio

from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
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
            input=row.input,
            actual_output=your_ai_func_result(row.input)["actual output"],
            expected_output=row.expected_output,
            retrieved_context=your_ai_func_result(row.input)["retrieved_context"],
        )
        for row in DictDataset.from_csv("dataset_examples/simple_qa_data.csv").load()
    ]
    suite = EvalSuite(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
    )
    results = await evaluate_suites(
        suites=[suite],
        experiment_tracker=CSVExperimentTracker(project_name="evals_test"),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
