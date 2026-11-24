"""Example of using the GoogleSheetsExperimentTracker with evaluate_suites.

References:
    NONE
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.google_sheets_experiment_tracker import (
    GoogleSheetsExperimentTracker,
    GoogleSheetsTrackerConfig,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def main():
    """Demonstrate experiment tracking with GoogleSheetsExperimentTracker."""
    load_dotenv()
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.environ["OPENROUTER_API_KEY"],
        config={"provider": {"order": ["inference-net"], "allow_fallbacks": False}},
    )
    config = GoogleSheetsTrackerConfig(
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )

    tracker = GoogleSheetsExperimentTracker(
        project_name="my_evals",
        config=config,
        score_key="score",
    )

    suite = EvalSuite(
        name="my_evals",
        data=DictDataset.from_jsonl(
            str(Path(__file__).parent / "dataset_examples" / "simple_rag_data.jsonl")
        ),
        evaluators=[GEvalGenerationEvaluator(models=model)],
    )

    result = await evaluate_suites(
        suites=[suite],
        experiment_tracker=tracker,
    )

    print(f"Run ID: {result.run_id}")
    print(f"Run worksheet: {result.experiment_uris.run_uri}")
    print(f"Leaderboard: {result.experiment_uris.leaderboard_uri}")


if __name__ == "__main__":
    asyncio.run(main())
