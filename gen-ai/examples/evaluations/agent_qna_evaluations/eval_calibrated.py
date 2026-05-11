"""Example script to evaluate an AI agent pipeline with calibrated metrics.

Calibration: replace GEvalCompletenessMetric with GEvalContextSufficiencyMetric
for multi-value enumeration queries (Cases 1 and 3).

Reasoning:
- Supported platform and language lists grow with each product release, so a
  fixed expected_output becomes stale quickly.
- Multiple valid answer sources exist (support varies by version, tier, region),
  so there is rarely one definitive reference to compare against.
- context_sufficiency checks whether tools_called returned sufficient data to
  answer the query — durable regardless of catalog size.

Case 2 (single-value lookup) keeps the default evaluator. Single-fact answers
have a stable, single-source reference where completeness is appropriate.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import LLMTestCase, evaluate
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.retrieval.geval_context_sufficiency import GEvalContextSufficiencyMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATASET = DictDataset.from_csv("data/eval_dataset.csv").load()
OUTPUT_DIR = "results"

# Mock agent outputs: only runtime agent data lives here.
MOCK_AGENT_OUTPUTS: dict[str, tuple[str, list[dict]]] = {
    "What cloud platforms does CloudDeploy Pro support?": (
        "CloudDeploy Pro supports AWS, Google Cloud, and Azure.",
        [
            {
                "name": "get_product_integrations",
                "input_parameters": {"product": "CloudDeploy Pro"},
                "output": {
                    # Note: DigitalOcean and Heroku absent — tool retrieval gap
                    "supported_platforms": ["AWS", "Google Cloud", "Azure"],
                },
            }
        ],
    ),
    "What is the delivery date for order ORD-7743?": (
        "Order ORD-7743 is scheduled for delivery on May 20th, 2025.",
        [
            {
                "name": "get_order_status",
                "input_parameters": {"order_id": "ORD-7743"},
                "output": {
                    "order_id": "ORD-7743",
                    "status": "processing",
                    "estimated_delivery": "May 20th, 2025",
                    "carrier": "FastShip Express",
                },
            }
        ],
    ),
    "What programming languages does CodeScan support?": (
        "CodeScan supports Python, JavaScript, TypeScript, Java, and Go.",
        [
            {
                "name": "get_supported_languages",
                "input_parameters": {"product": "CodeScan"},
                "output": {
                    # Note: Ruby and Rust absent — tool retrieval gap
                    "supported_languages": [
                        "Python", "JavaScript", "TypeScript", "Java", "Go"
                    ],
                },
            }
        ],
    ),
}


def run_agent(query: str) -> tuple[str, str]:
    """Return mock agent output for a query.

    Returns:
        (actual_output, retrieved_context) where retrieved_context
        is a JSON-serialized list of tools_called payloads.
    """
    actual_output, tools_called = MOCK_AGENT_OUTPUTS[query]
    return actual_output, json.dumps(tools_called)


async def main():
    agent_results = [run_agent(row["query"]) for row in DATASET]

    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=actual_output,
            expected_output=row["expected_output"],
            retrieved_context=retrieved_context,
        )
        for row, (actual_output, retrieved_context) in zip(DATASET, agent_results)
    ]

    judge_model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    tracker = CSVExperimentTracker(
        project_name="agent-qna-eval",
        output_dir=OUTPUT_DIR,
        include_eval_result=True,
    )

    # Cases 1 and 3: multi-value enumeration queries — completeness replaced by
    # context_sufficiency. Supported items grow with each release
    result_multi = await evaluate(
        data=[data[0], data[2]],
        evaluators=[
            GEvalGenerationEvaluator(
                models=judge_model,
                metrics=[
                    GEvalContextSufficiencyMetric(),  # replaces completeness
                    GEvalGroundednessMetric(),
                    GEvalRedundancyMetric(),
                ],
            )
        ],
        experiment_tracker=tracker,
    )
    print(result_multi)

    # Step 2b: Case 2 — default evaluation (completeness + groundedness + redundancy).
    result_single = await evaluate(
        data=[data[1]],
        evaluators=[GEvalGenerationEvaluator(models=judge_model)],
        experiment_tracker=tracker,
    )
    print(result_single)


if __name__ == "__main__":
    asyncio.run(main())
