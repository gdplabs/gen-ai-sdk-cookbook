"""An example of evaluating multiple data partitions using evaluate_suites.

This example demonstrates three suites with test cases loaded from local data files:
- qa: Simple Q&A evaluation (generation evaluator)
- rag: RAG evaluation with groundedness evaluator
- agent: Agent tool-use evaluation (includes tools_called/expected_tools)

Authors:
    - Kalvin (kalvinsupriadi3@gmail.com)

References:
    [1] None
"""

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"


def _to_eval_row(row: dict) -> LLMTestCase:
    """Map dataset columns to evaluation input keys."""
    return LLMTestCase(
        input=row["query"],
        actual_output=row["generated_response"],
        expected_output=row["expected_response"],
        retrieved_context=row.get("retrieved_context") or None,
        tools_called=row.get("tools_called"),
        expected_tools=row.get("expected_tools"),
    )


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id=DefaultValues.MODEL,
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    qa_suite = EvalSuite(
        name="qa",
        data=[_to_eval_row(r) for r in DictDataset.from_csv(path=DATA_DIR / "simple_qa_data.csv").load()],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    rag_suite = EvalSuite(
        name="rag",
        data=[_to_eval_row(r) for r in DictDataset.from_csv(path=DATA_DIR / "simple_rag_data.csv").load()],
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            )
        ],
    )

    agent_data_raw = json.loads((DATA_DIR / "simple_agent_tool_call_data.json").read_text())
    agent_suite = EvalSuite(
        name="agent",
        data=[
            _to_eval_row(r)
            for r in DictDataset(agent_data_raw).load()
            if r.get("tools_called") and r.get("expected_tools")
        ],
        evaluators=[AgentEvaluator(models=[judge_model])],
    )

    result = await evaluate_suites(
        suites=[qa_suite, rag_suite, agent_suite],
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
