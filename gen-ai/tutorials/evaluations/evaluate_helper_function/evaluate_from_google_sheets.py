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
from gllm_evals import LLMTestCase
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from your_ai_func_result import your_ai_func_result

load_dotenv()


async def main() -> None:
    """Run evaluation with Google Sheets as the data source.

    This example demonstrates how to:
    - Load data from Google Sheets
    - Convert to standard format and construct LLMTestCase objects
    """
    dataset = (
        await SpreadsheetDataset.from_gsheets(
            sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
            worksheet_name="test_dataset",
            client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
            private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
        )
    ).to_standard_format()

    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in dataset
    ]

    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
