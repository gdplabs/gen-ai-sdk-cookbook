import asyncio
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from inference_mock import your_ai_func_result

load_dotenv()


async def main() -> None:
    """Run evaluate_suites with Google Sheets as the data source.

    This example demonstrates how to:
    - Load data from Google Sheets as LLMTestCase rows
    - Add the output of your AI system to each row
    - Evaluate the rows as one EvalSuite
    """
    dataset = await SpreadsheetDataset.from_gsheets(
        sheet_id=os.environ["GOOGLE_SHEETS_SHEET_ID"],
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )

    data = []
    for row in dataset.load():
        ai_result = your_ai_func_result(row.input)
        data.append(
            row.model_copy(
                update={
                    "actual_output": ai_result["actual output"],
                    "retrieved_context": ai_result["retrieved_context"],
                }
            )
        )

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
