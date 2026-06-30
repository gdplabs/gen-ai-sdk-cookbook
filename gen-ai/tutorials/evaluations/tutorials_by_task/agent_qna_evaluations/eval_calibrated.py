"""Example script to evaluate an AI agent pipeline with calibrated metrics.

Calibration for multi-value enumeration queries (Cases 1 and 3):
- Replace completeness with tool_correctness + context_sufficiency.
- tool_correctness: validates the agent called the right tool with the right
  input arguments — a behavioral check on the agent's routing decision.
- context_sufficiency: validates the tool's response contained enough data to
  fully answer the query — a data quality check on the retrieval layer.
- Together they enable root cause attribution: if tool_correctness passes but
  context_sufficiency fails, the agent routed correctly but the tool returned
  incomplete data → fix the tool, not the agent.

Case 2 (single-value lookup) keeps the default evaluator. Single-fact answers
have a stable, single-source reference where completeness is appropriate.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle
"""

import asyncio
import json

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.retrieval.geval_context_sufficiency import (
    GEvalContextSufficiencyMetric,
)
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import (
    DeepEvalToolCorrectnessMetric,
)
from gllm_evals.types import ToolCall
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

import csv as csv_mod

with open("data/eval_dataset.csv", newline="") as f:
    rows = list(csv_mod.DictReader(f))
DATASET = [
    {
        "input": row["input"],
        "expected_output": row["expected_output"],
        "expected_tools": json.loads(row["expected_tools"]),
    }
    for row in rows
]
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
                        "Python",
                        "JavaScript",
                        "TypeScript",
                        "Java",
                        "Go",
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
    agent_results = [run_agent(row["input"]) for row in DATASET]

    data = [
        LLMTestCase(
            input=row["input"],
            actual_output=actual_output,
            expected_output=row["expected_output"],
            retrieved_context=retrieved_context,
            tools_called=ToolCall.from_dicts(tools_called_list),
            expected_tools=ToolCall.from_dicts(row["expected_tools"]),
        )
        for row, (actual_output, tools_called_list, retrieved_context) in zip(
            DATASET, agent_results
        )
    ]

    judge_model = build_lm_invoker(model_id=DefaultValues.MODEL)
    tracker = CSVExperimentTracker(
        project_name="agent-qna-eval",
        output_dir=OUTPUT_DIR,
        include_eval_result=True,
    )

    result = await evaluate_suites(
        suites=[
            # Cases 1 and 3: tool_correctness checks agent routing, context_sufficiency
            # checks tool data quality. Together they attribute failures to the right layer.
            EvalSuite(
                name="multi_metric",
                data=[data[0], data[2]],
                evaluators=[
                    GEvalGenerationEvaluator(
                        models=judge_model,
                        metrics=[
                            DeepEvalToolCorrectnessMetric(),  # verify tool name only
                            GEvalContextSufficiencyMetric(),  # tool data sufficiency check
                            GEvalGroundednessMetric(),
                            GEvalRedundancyMetric(),
                        ],
                    )
                ],
            ),
            # Case 2: single-value lookup — default (completeness + groundedness + redundancy).
            EvalSuite(
                name="single_lookup",
                data=[data[1]],
                evaluators=[GEvalGenerationEvaluator(models=judge_model)],
            ),
        ],
        experiment_tracker=tracker,
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
