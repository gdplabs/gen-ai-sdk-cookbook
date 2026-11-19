"""Example of using the GoogleSheetsExperimentTracker with evaluate_suites.

References:
    NONE
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset import load_simple_rag_dataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.google_sheets_experiment_tracker import (
    GoogleSheetsExperimentTracker,
    GoogleSheetsTrackerConfig,
)


async def main():
    """Demonstrate experiment tracking with GoogleSheetsExperimentTracker."""
    load_dotenv()
    project_name = f"my_evals_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    config = GoogleSheetsTrackerConfig(
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )

    tracker = GoogleSheetsExperimentTracker(
        project_name=project_name,
        config=config,
        score_key="score",
    )

    suite = EvalSuite(
        name="my_evals",
        data=load_simple_rag_dataset(current_dir=Path(__file__).parent / "dataset_examples"),
        evaluators=[GEvalGenerationEvaluator()],
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
