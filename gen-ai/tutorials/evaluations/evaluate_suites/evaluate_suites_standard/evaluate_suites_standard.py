"""An example of evaluating multiple data partitions using evaluate_suites.

This example demonstrates two suites with test cases loaded from local data files:
- qa: Simple Q&A evaluation (generation evaluator)
- agent: Agent tool-use evaluation (includes tools_called/expected_tools)

References:
    [1] None
"""

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"


def _to_eval_row(row: LLMTestCase) -> LLMTestCase:
    """Map dataset columns to evaluation input keys."""
    return LLMTestCase(
        input=row.query,
        actual_output=row.generated_response,
        expected_output=row.expected_response,
        retrieved_context=row.retrieved_context or None,
        tools_called=row.tools_called,
        expected_tools=row.expected_tools,
    )


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )

    qa_data = DictDataset.from_csv(path=DATA_DIR / "simple_qa_data.csv").load()
    agent_data = json.loads((DATA_DIR / "simple_agent_tool_call_data.json").read_text())

    qa_suite = EvalSuite(
        name="qa",
        data=[_to_eval_row(r) for r in qa_data],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    agent_suite = EvalSuite(
        name="agent",
        data=[_to_eval_row(r) for r in DictDataset(agent_data).load()],
        evaluators=[CompositeEvaluator(
            name="agent",
            metrics=[
                DeepEvalToolCorrectnessMetric(models=judge_model),
                GEvalCompletenessMetric(models=judge_model),
                GEvalGroundednessMetric(models=judge_model),
                GEvalRedundancyMetric(models=judge_model),
            ],
        )],
    )

    result = await evaluate_suites(
        suites=[qa_suite, agent_suite],
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
