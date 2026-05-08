"""Evaluate Helper Function Example - Standard Dataset.

This tutorial demonstrates how to use the `evaluate()` convenience helper function
with standard datasets (local files or built-in datasets).

The evaluate() function supports:
- Structured evaluation rules (each record receives the same evaluation treatment)
- Multiple data sources (HuggingFace, Langfuse, local files)
- Custom inference functions
- Multiple evaluators
- Experiment tracking
- Summary evaluators for aggregate metrics
"""

import asyncio

from gllm_evals import LLMTestCase, load_simple_qa_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from your_ai_func_result import your_ai_func_result


async def main() -> None:
    """Run evaluation with the built-in simple QA dataset.

    This example demonstrates the basic usage of evaluate() with:
    - Built-in dataset loader
    - Default inference function
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
        for row in load_simple_qa_dataset().load()
    ]
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
        experiment_tracker=CSVExperimentTracker(project_name="evals_test"),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
