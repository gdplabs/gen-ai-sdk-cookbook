import asyncio
import json

from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.types import EvaluatorResult, MetricInput
from inference_mock import your_ai_func_result


def accuracy_summary(
    evaluation_results: list[list[EvaluatorResult]], data: list[MetricInput]
) -> dict[str, float]:
    """Compute average accuracy from evaluation results.

    Args:
        evaluation_results: Row-grouped evaluation outputs from the batch.
        data: List of input data for the batch.

    Returns:
        Dict containing the average accuracy score.
    """
    weighted_average_list = []
    for row_results in evaluation_results:
        evaluation_result = next(
            result for result in row_results if "generation" in result
        )
        generation_result = evaluation_result["generation"]
        weighted_average = (
            generation_result["completeness"]["score"]
            + generation_result["redundancy"]["score"] * 3
        ) / 2
        weighted_average_list.append(weighted_average)

    return {"weighted_average": sum(weighted_average_list) / len(weighted_average_list)}


async def main():
    """Main function demonstrating summary evaluators."""
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in DictDataset.from_csv("dataset_examples/simple_qa_data.csv").load()
    ]
    suite = EvalSuite(
        data=data,
        evaluators=[
            GEvalGenerationEvaluator(
                metrics=[GEvalCompletenessMetric(), GEvalRedundancyMetric()]
            )
        ],
    )
    result = await evaluate_suites(
        suites=[suite],
        run_aggregators=[
            accuracy_summary,
        ],
        batch_size=1,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
