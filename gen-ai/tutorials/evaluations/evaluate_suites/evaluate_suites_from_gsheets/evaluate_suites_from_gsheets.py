"""Example script for evaluate_suites using Google Sheets as data source.

Authors:
Kalvin (kalvinsupriadi3@gmail.com)
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


async def main() -> None:
    """Run evaluate_suites with data loaded from Google Sheets."""
    judge_model = build_lm_invoker(
        model_id="openai/gpt-5-nano",
        credentials=os.getenv("OPENAI_API_KEY"),
    )

    # Load QA data from Google Sheets
    qa_dataset = (
        await SpreadsheetDataset.from_gsheets(
            sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
            worksheet_name="qa_dataset",
            client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
            private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
        )
    ).to_standard_format()

    qa_data = [
        LLMTestCase(
            input=row["query"],
            actual_output=row["actual_output"],
            expected_output=row["expected_response"],
            retrieved_context=row["retrieved_context"],
        )
        for row in qa_dataset
    ]

    # Load RAG data from Google Sheets (different worksheet)
    rag_dataset = (
        await SpreadsheetDataset.from_gsheets(
            sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
            worksheet_name="rag_dataset",
            client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
            private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
        )
    ).to_standard_format()

    rag_data = [
        LLMTestCase(
            input=row["query"],
            actual_output=row["actual_output"],
            expected_output=row["expected_response"],
            retrieved_context=row["retrieved_context"],
        )
        for row in rag_dataset
    ]

    qa_suite = EvalSuite(
        name="qa",
        data=qa_data,
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    rag_suite = EvalSuite(
        name="rag",
        data=rag_data,
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            )
        ],
    )

    result = await evaluate_suites(
        suites=[qa_suite, rag_suite],
        dataset_name="gsheets_multi_suite",
    )
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
