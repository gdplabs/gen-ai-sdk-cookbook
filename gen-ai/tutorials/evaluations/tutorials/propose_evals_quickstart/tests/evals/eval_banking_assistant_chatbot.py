"""Score every case of the Banking Assistant Chatbot dataset with evaluate_suites and record every score. No pass/fail gate.

Runs the chatbot once per case (each call costs money), then scores each suite with its metrics.
Run: `python tests/evals/eval_banking_assistant_chatbot.py` from the tutorial root.
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT: Path = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(1, str(ROOT / "chatbot"))

from banking_assistant_chatbot_assignment import suite_of  # noqa: E402
from evaluators import build_evaluators  # noqa: E402

from gllm_evals import EvalSuite, evaluate_suites  # noqa: E402
from gllm_evals.dataset.dict_dataset import DictDataset  # noqa: E402
from gllm_evals.experiment_tracker import JSONExperimentTracker  # noqa: E402
from gllm_evals.types import LLMTestCase  # noqa: E402

DATASET_PATH: Path = ROOT / "data" / "data.jsonl"
OUTPUT_DIR: Path = Path(__file__).resolve().parent / "results"
FIELD_MAPPING = {"question": "input", "context": "retrieved_context", "expected_response": "expected_output"}


async def run_target(chatbot, case: LLMTestCase) -> LLMTestCase:
    """Ask the chatbot the case's question with its policy context; its final answer becomes actual_output."""
    result = await chatbot.answer({"question": case.input, "context": case.retrieved_context})
    return case.model_copy(update={"actual_output": result["generated_response"]})


async def main() -> None:
    """Run the target on every case, score each suite, and record the results."""
    from banking_assistant_chatbot import BankingAssistantChatbot  # the target, imported unchanged

    evaluators = build_evaluators()
    cases = DictDataset.from_jsonl(str(DATASET_PATH), id_column="id", field_mapping=FIELD_MAPPING).load()
    for case in cases:  # stop before any target call on a case with no suite
        if (suite := suite_of(case)) not in evaluators:
            raise ValueError(f"{case.test_case_id}: no suite (got {suite!r}). Add an evaluator for it, or fix its suite.")

    chatbot = BankingAssistantChatbot()
    cases_by_suite: dict[str, list[LLMTestCase]] = {}
    unscored: dict[str, str] = {}
    for case in cases:  # one target call per case
        try:
            cases_by_suite.setdefault(suite_of(case), []).append(await run_target(chatbot, case))
        except Exception as error:  # noqa: BLE001 - one case's target failure must not lose the run
            unscored[case.test_case_id] = repr(error)

    result = await evaluate_suites(
        suites=[
            EvalSuite(name=suite, data=suite_cases, evaluators=evaluators[suite])
            for suite, suite_cases in cases_by_suite.items()
        ],
        experiment_tracker=JSONExperimentTracker(project_name="banking-assistant-chatbot", output_dir=str(OUTPUT_DIR)),
    )
    for name, suite in result.suites.items():
        print(f"{name}: {suite.run_aggregators_result}")
    for case_id, why in unscored.items():
        print(f"{case_id}: not scored, the target raised {why}")
    if unscored:
        raise SystemExit(f"{len(unscored)} case(s) not scored")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
