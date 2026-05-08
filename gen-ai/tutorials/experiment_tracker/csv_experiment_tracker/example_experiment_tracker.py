"""Example of using the CSVExperimentTracker with the evaluate function.

Authors:
    Apri Dwi Rachmadi (apri.d.rachmadi@gdplabs.id)

References:
    NONE
"""

import asyncio

from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.types import LLMTestCase
from gllm_evals.utils.shared_functionality import generate_run_id_if_not_provided


async def main():
    """Demonstrate experiment tracking with CSVExperimentTracker."""
    tracker = CSVExperimentTracker(
        "my_project", output_dir="./my_experiments", score_key="score"
    )

    dataset = [
        LLMTestCase(
            input="What is the capital of France?",
            expected_output="Paris",
            actual_output="New York",
            retrieved_context="Paris is the capital of France.",
        ),
        LLMTestCase(
            input="What is 1 + 1?",
            expected_output="2",
            actual_output="2",
            retrieved_context="1 + 1 = 2",
        ),
    ]

    evaluator = GEvalGenerationEvaluator()

    metadata = {
        "evaluator_name": "generation",
        "batch_size": 10,
        "parallel": True,
        "model_name": DefaultValues.MODEL,
        "evaluator_versions": {"generation": "1.0.0"},
    }

    try:
        run_id = generate_run_id_if_not_provided(
            tracker.project_name, "sample_qa_dataset", None
        )

        for i, data in enumerate(dataset):
            evaluator_results = await evaluator.evaluate(data)

            row_metadata = {**metadata, "row_index": i, "dataset_size": len(dataset)}

            print(evaluator_results)
            print(data)

            tracker.log(
                evaluation_result=evaluator_results,
                dataset_name="sample_qa_dataset",
                data=data,
                metadata=row_metadata,
                run_id=run_id,
            )

        results = tracker.get_run_results(run_id)[0]
        print(results)

    except Exception as e:
        print(f"Experiment failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
