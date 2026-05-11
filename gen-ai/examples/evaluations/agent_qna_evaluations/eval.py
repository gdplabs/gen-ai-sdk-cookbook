"""Example script to evaluate an AI agent pipeline using mock tool call outputs.

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
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

# Step 2: Prepare Dataset
# Load from CSV — each row has "query" and "expected_output".
DATASET = DictDataset.from_csv("data/eval_dataset.csv").load()
OUTPUT_DIR = "results"

# Mock agent outputs keyed by query.
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
    # Step 4: Run the agent for every case
    agent_results = [run_agent(row["query"]) for row in DATASET]

    # Build LLMTestCase list — CSV provides input/expected_output,
    # agent mock provides actual_output/retrieved_context (serialized tool calls)
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
    experiment_result = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=judge_model)],
        experiment_tracker=tracker,
    )
    print(experiment_result)


if __name__ == "__main__":
    asyncio.run(main())
