"""An example of evaluating multiple data partitions using evaluate_suites.

This example demonstrates two suites with test cases loaded from local data files:
- qa: Simple Q&A evaluation (generation evaluator)
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
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id=DefaultValues.MODEL,
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    qa_data = DictDataset.from_csv(path=DATA_DIR / "simple_qa_data.csv").load()
    agent_data = json.loads((DATA_DIR / "simple_agent_tool_call_data.json").read_text())

    qa_suite = EvalSuite(
        name="qa",
        data=qa_data,
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    agent_suite = EvalSuite(
        name="agent",
        data=DictDataset(agent_data).load(),
        evaluators=[AgentEvaluator(models=[judge_model])],
    )

    result = await evaluate_suites(
        suites=[qa_suite, agent_suite],
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
