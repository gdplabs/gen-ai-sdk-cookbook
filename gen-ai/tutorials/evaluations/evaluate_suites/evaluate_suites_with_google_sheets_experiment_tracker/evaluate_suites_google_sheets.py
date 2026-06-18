"""Example of using evaluate_suites for evaluating multiple data partitions.

The evaluate_suites function allows you to evaluate different data partitions (suites)
with different evaluators, while sharing a single run_id and experiment tracker.
Each suite's dataset name is automatically namespaced.

This is useful for:
- Evaluating different model types on different datasets
- Running different evaluation strategies on different data partitions
- Comparing results across multiple evaluation configurations

Authors:
    Mikhael Chris (mikhael.chris@gdplabs.id)

References:
    NONE
"""

import os
import asyncio
import json

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.experiment_tracker.google_sheets_experiment_tracker import (
    GoogleSheetsExperimentTracker,
    GoogleSheetsTrackerConfig,
)
from gllm_evals.aggregation.run_aggregators import (
    summary_accuracy,
    true_negative_rate,
    true_positive_rate,
)


async def main():
    """Run evaluate_suites with different evaluators for different data suites."""
    load_dotenv()
    # Suite 1: General knowledge questions with generation evaluator
    qa_suite = EvalSuite(
        name="qa",
        data=[
            LLMTestCase(
                input="What is the capital of France?",
                actual_output="Paris is the capital of France.",
                expected_output="Paris",
                retrieved_context="France is a country in Europe. Paris is the largest city.",
                label=True,
            ),
            LLMTestCase(
                input="What is the largest planet in our solar system?",
                actual_output="Mars is the largest planet.",
                expected_output="Jupiter",
                retrieved_context="Jupiter is the fifth planet from the Sun.",
                label=False,
            ),
        ],
        evaluators=[GEvalGenerationEvaluator()],
    )

    # Suite 2: Retrieved context evaluation with groundedness evaluator
    rag_suite = EvalSuite(
        name="rag",
        data=[
            LLMTestCase(
                input="What year was the Eiffel Tower built?",
                actual_output="The Eiffel Tower was built in 1889.",
                expected_output="1889",
                retrieved_context="The Eiffel Tower, built for the 1889 World's Fair in Paris, is an iconic iron lattice tower.",  # noqa: E501
                label=True,
            ),
            LLMTestCase(
                input="Who wrote Romeo and Juliet?",
                actual_output="William Shakespeare wrote Romeo and Juliet.",
                expected_output="William Shakespeare",
                retrieved_context="Romeo and Juliet is a tragedy written by William Shakespeare early in his career.",
                label=True,
            ),
        ],
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric()],
                name="groundedness",
            )
        ],
    )

    # Suite 3: Auto-generated suite name with generation evaluator
    auto_named_suite = EvalSuite(
        data=[
            LLMTestCase(
                input="What is 2 + 2?",
                actual_output="2 + 2 equals 4.",
                expected_output="4",
                label=True,
            ),
        ],
        evaluators=[GEvalGenerationEvaluator()],
    )

    # Run evaluate_suites with all three suites
    # Each suite uses its own evaluators, but they share:
    # - A single run_id
    # - A shared experiment tracker
    # - A base dataset name (with per-suite namespacing)
    client_email = os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL")
    private_key = os.getenv("GOOGLE_SHEETS_PRIVATE_KEY", "").replace("\\n", "\n")
    config = GoogleSheetsTrackerConfig(
        client_email=client_email,
        private_key=private_key,
    )
    result = await evaluate_suites(
        suites=[qa_suite, rag_suite, auto_named_suite],
        dataset_name="multi_suite_evaluation",
        experiment_tracker=GoogleSheetsExperimentTracker(
            project_name="demo-project",
            config=config,
        ),
        run_aggregators=[summary_accuracy, true_negative_rate, true_positive_rate],
    )

    # Print results
    print("\n" + "=" * 60)
    print("EVALUATE_SUITES RESULTS")
    print("=" * 60)
    print(f"\nRun ID: {result.run_id}")
    print(f"Base Dataset Name: {result.dataset_name}")
    print(f"Total Samples Evaluated: {result.num_samples}")
    print(f"Timestamp: {result.timestamp}")

    print("\n" + "-" * 60)
    print("PER-SUITE RESULTS")
    print("-" * 60)

    for suite_name, suite_result in result.suites.items():
        print(f"\nSuite: {suite_name}")
        print(f"  Dataset Name: {suite_result.dataset_name}")
        print(f"  Samples: {suite_result.num_samples}")
        print(f"  Aggregator Results: {suite_result.run_aggregators_result}")
        print(f"  Results: {json.dumps(suite_result.results, indent=2)}")

    print("\n" + "-" * 60)
    print("TOP-LEVEL POOLED RESULTS")
    print("-" * 60)
    print("\nAggregator Results (all suites pooled):")
    print(json.dumps(result.run_aggregators_result, indent=2))

    print("\n" + "=" * 60)
    print("Experiment URIs:")
    print(json.dumps(result.experiment_uris, indent=2))

    print("\n" + "=" * 60)
    print("Full Result:")
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
