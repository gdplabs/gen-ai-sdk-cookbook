import asyncio
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from inference_mock import your_ai_func_result

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
            input=row.input,
            actual_output=your_ai_func_result(row.input)["actual output"],
            expected_output=row.expected_output,
            retrieved_context=your_ai_func_result(row.input)["retrieved_context"],
        )
        for row in dataset
    ]

    suite = EvalSuite(
        data=data,
        evaluators=[GEvalGenerationEvaluator()],
    )
    results = await evaluate_suites(
        suites=[suite],
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
