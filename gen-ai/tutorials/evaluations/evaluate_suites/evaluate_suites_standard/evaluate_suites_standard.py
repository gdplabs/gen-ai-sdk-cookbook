"""An example of evaluating multiple data partitions using evaluate_suites with built-in datasets.

This example demonstrates three suites using built-in datasets from gllm-evals:
- qa: Simple Q&A evaluation using load_simple_qa_dataset
- rag: RAG evaluation with groundedness using load_simple_rag_dataset
- agent: Agent tool-use evaluation using load_simple_agent_tool_call_dataset
  (includes tools_called/expected_tools in the LLMTestCase data)

Authors:
    - Kalvin (kalvinsupriadi3@gmail.com)

References:
    [1] None
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset import (
    load_simple_agent_tool_call_dataset,
    load_simple_qa_dataset,
    load_simple_rag_dataset,
)
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


def _to_eval_row(row: dict) -> dict:
    """Map built-in dataset columns to evaluation input keys."""
    return {
        "input": row["query"],
        "actual_output": row["generated_response"],
        "expected_output": row["expected_response"],
        "retrieved_context": row.get("retrieved_context") or None,
        "tools_called": row.get("tools_called"),
        "expected_tools": row.get("expected_tools"),
    }


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    qa_suite = EvalSuite(
        name="qa",
        data=[_to_eval_row(r) for r in load_simple_qa_dataset().load()],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    rag_suite = EvalSuite(
        name="rag",
        data=[_to_eval_row(r) for r in load_simple_rag_dataset().load()],
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            )
        ],
    )

    agent_suite = EvalSuite(
        name="agent",
        data=[_to_eval_row(r) for r in load_simple_agent_tool_call_dataset().load()],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    result = await evaluate_suites(
        suites=[qa_suite, rag_suite, agent_suite],
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
