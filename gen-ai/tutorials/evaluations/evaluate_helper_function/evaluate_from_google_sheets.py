"""Evaluate Helper Function Example - Google Sheets Dataset.

This tutorial demonstrates how to use the `evaluate()` convenience helper function
with Google Sheets as the data source.

The evaluate() function supports:
- Structured evaluation rules (each record receives the same evaluation treatment)
- Multiple data sources (HuggingFace, Google Sheets, Langfuse, local files)
- Custom inference functions
- Multiple evaluators
- Experiment tracking with Langfuse
- Summary evaluators for aggregate metrics
"""

import asyncio
import os

from dotenv import load_dotenv
from langfuse import get_client

from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import (
    LangfuseExperimentTracker,
)
from gllm_evals.utils.shared_functionality import inference_fn

load_dotenv()


async def main() -> None:
    """Run evaluation with Google Sheets as the data source.

    This example demonstrates how to:
    - Load data from Google Sheets
    - Use Langfuse for experiment tracking
    - Map spreadsheet columns to evaluation fields

    Prerequisites:
    - Set up Google Sheets API credentials in .env:
      - GOOGLE_SHEETS_CLIENT_EMAIL
      - GOOGLE_SHEETS_PRIVATE_KEY
    - Set up Langfuse credentials in .env:
      - LANGFUSE_PUBLIC_KEY
      - LANGFUSE_SECRET_KEY
      - LANGFUSE_BASE_URL
    - Set up value for google_sheet_id and langfuse_project_name
    """
    google_sheet_id = "YOUR_GOOGLE_SHEET_ID"
    langfuse_project_name = "YOUR_LANGFUSE_PROJECT_NAME"

    # Define the mapping between spreadsheet columns and evaluation fields
    mapping = {
        "input": {
            "question_id": "question_id",
            "query": "query",
            "retrieved_context": "retrieved_context",
            "generated_response": "generated_response",
        },
        "expected_output": {"expected_response": "expected_response"},
        "metadata": {"topic": "topic"},
    }

    results = await evaluate(
        data=await SpreadsheetDataset.from_gsheets(
            sheet_id=google_sheet_id,
            worksheet_name="new-test",
            client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
            private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
        ),
        inference_fn=inference_fn,
        evaluators=[
            GEvalGenerationEvaluator(model_credentials=os.getenv("GOOGLE_API_KEY"))
        ],
        experiment_tracker=LangfuseExperimentTracker(
            langfuse_client=get_client(),
            mapping=mapping,
            project_name=langfuse_project_name,
        ),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
