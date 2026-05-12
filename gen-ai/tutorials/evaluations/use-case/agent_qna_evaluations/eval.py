"""Example script to evaluate an AI agent pipeline using mock tool call outputs.

The dataset includes expected_tools, so DeepEvalToolCorrectnessMetric is included
in the initial evaluation alongside the default generation metrics. This gives an
early signal on agent routing correctness before any calibration is applied.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from deepeval.test_case import ToolCallParams
from gllm_evals import LLMTestCase, evaluate
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_evals.types import ToolCall
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


def run_agent(query: str) -> tuple[str, list[dict], str]:
    """Return mock agent output for a query.

    Returns:
        (actual_output, tools_called, retrieved_context) where tools_called is
        the raw list of tool call dicts and retrieved_context is its JSON form.
    """
    actual_output, tools_called = MOCK_AGENT_OUTPUTS[query]
    return actual_output, tools_called, json.dumps(tools_called)


async def main():
    # Step 4: Run the agent for every case
    agent_results = [run_agent(row["query"]) for row in DATASET]

    # Build LLMTestCase list — CSV provides input/expected_output/expected_tools,
    # agent mock provides actual_output/tools_called/retrieved_context
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=actual_output,
            expected_output=row["expected_output"],
            retrieved_context=retrieved_context,
            tools_called=ToolCall.from_dicts(tools_called_list),
            expected_tools=ToolCall.from_dicts(json.loads(row["expected_tools"])),
        )
        for row, (actual_output, tools_called_list, retrieved_context) in zip(DATASET, agent_results)
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
    # Use default generation metrics + tool_correctness (dataset has expected_tools).
    # evaluation_params limits comparison to name + args; expected_tools has no output.
    experiment_result = await evaluate(
        data=data,
        evaluators=[
            GEvalGenerationEvaluator(
                models=judge_model,
                metrics=[
                    DeepEvalToolCorrectnessMetric(
                        evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
                    ),
                    GEvalCompletenessMetric(),
                    GEvalGroundednessMetric(),
                    GEvalRedundancyMetric(),
                ],
            )
        ],
        experiment_tracker=tracker,
    )
    print(experiment_result)


if __name__ == "__main__":
    asyncio.run(main())
