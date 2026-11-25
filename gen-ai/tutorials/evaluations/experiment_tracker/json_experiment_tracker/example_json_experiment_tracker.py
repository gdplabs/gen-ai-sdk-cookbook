"""Log individual evaluations with JSONExperimentTracker and read the saved run history."""

import asyncio
import os
from uuid import uuid4

from dotenv import load_dotenv
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.json_experiment_tracker import JSONExperimentTracker
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main():
    """Demonstrate experiment tracking with JSONExperimentTracker."""
    load_dotenv()
    tracker = JSONExperimentTracker(
        project_name="my_project", output_dir="./my_experiments"
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

    model_id = "openrouter/deepseek/deepseek-v4.1-flash-1017"
    model = build_lm_invoker(
        model_id=model_id,
        credentials=os.environ["OPENROUTER_API_KEY"],
        config={"provider": {"order": ["inference-net"], "allow_fallbacks": False}},
    )
    evaluator = GEvalGenerationEvaluator(models=model)

    metadata = {
        "evaluator_name": evaluator.name,
        "model_name": model_id,
    }

    run_id = uuid4().hex
    for i, data in enumerate(dataset):
        evaluator_results = await evaluator.evaluate(data)

        row_metadata = {**metadata, "row_index": i, "dataset_size": len(dataset)}

        tracker.log(
            evaluation_result=evaluator_results,
            dataset_name="sample_qa_dataset",
            data=data,
            metadata=row_metadata,
            run_id=run_id,
        )
        print(f"Logged row {i + 1}/{len(dataset)}")

    for summary in tracker.get_run_results(run_id):
        print(f"Run {run_id}: {summary['total_results']} saved rows, average score {summary['average_score']}")

    print("Project history (most recent first)")
    for entry in tracker.get_experiment_history():
        print(f"{entry['run_id']}: average score {entry['average_score']}")


if __name__ == "__main__":
    asyncio.run(main())
