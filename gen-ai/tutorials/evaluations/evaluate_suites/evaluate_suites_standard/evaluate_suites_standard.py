"""An example of evaluating multiple data partitions using evaluate_suites.

This example demonstrates two suites with test cases loaded from local data files:
- qa: Simple Q&A evaluation (generation evaluator)
- agent: Agent tool-use evaluation (includes tools_called/expected_tools)

References:
    [1] None
"""

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"

# Map the dataset columns to LLMTestCase fields.
FIELD_MAPPING = {
    "query": "input",
    "generated_response": "actual_output",
    "expected_response": "expected_output",
}


async def main() -> None:
    qa_suite = EvalSuite(
        name="qa",
        data=DictDataset.from_csv(path=str(DATA_DIR / "simple_qa_data.csv"), field_mapping=FIELD_MAPPING),
        evaluators=[GEvalGenerationEvaluator()],
    )

    agent_data = json.loads((DATA_DIR / "simple_agent_tool_call_data.json").read_text())
    agent_suite = EvalSuite(
        name="agent",
        data=DictDataset(agent_data, field_mapping=FIELD_MAPPING),
        evaluators=[
            GEvalGenerationEvaluator(
                metrics=[
                    DeepEvalToolCorrectnessMetric(),
                    GEvalCompletenessMetric(),
                    GEvalGroundednessMetric(),
                    GEvalRedundancyMetric(),
                ]
            )
        ],
    )

    result = await evaluate_suites(
        suites=[qa_suite, agent_suite],
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
