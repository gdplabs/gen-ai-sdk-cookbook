"""An example of evaluating using evaluate_suites with Google Sheets as data source.

Data is loaded from a Google Sheet worksheet using SpreadsheetDataset,
then built into LLMTestCase objects with mock inference for demonstration.

Authors:
    - Kalvin (kalvinsupriadi3@gmail.com)

References:
    [1] evaluate_from_google_sheets.py — pattern reference for Google Sheets data loading
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_inference.lm_invoker import build_lm_invoker
from inference_mock import your_ai_func_result

load_dotenv()


async def main() -> None:
    judge_model = build_lm_invoker(
        model_id=DefaultValues.MODEL,
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

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
            input=row["input"],
            actual_output=your_ai_func_result(row["input"])["actual output"],
            expected_output=row["expected_output"],
            retrieved_context=your_ai_func_result(row["input"])["retrieved_context"],
        )
        for row in dataset
    ]

    suite = EvalSuite(
        name="gsheets",
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    result = await evaluate_suites(
        suites=[suite],
        dataset_name="gsheets_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
