import asyncio
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import (
    LangfuseExperimentTracker,
)
from inference_mock import your_ai_func_result
from langfuse import get_client

load_dotenv()


async def main() -> None:
    """Run evaluation with Langfuse experiment tracking.

    This example demonstrates how to:
    - Load data from Google Sheets
    - Use LangfuseExperimentTracker with custom mapping
    - Track evaluation results in Langfuse
    """
    mapping = {
        "input": {
            "question_id": "question_id",
            "query": "input",
            "retrieved_context": "retrieved_context",
            "generated_response": "generated_output",
        },
        "expected_output": {"expected_response": "expected_output"},
        "metadata": {"topic": "topic"},
    }

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
            question_id=row.question_id,
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
        experiment_tracker=LangfuseExperimentTracker(
            langfuse_client=get_client(),
            mapping=mapping,
        ),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
