"""Hardcoded question definitions for PoC evaluation."""

import os

from dotenv import load_dotenv
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset

load_dotenv()


async def load_dataset(
    query_ids: set[int] | None = None,
    question_ids: set[int] | None = None,
):
    """Load the dataset from Google Sheets.

    Args:
        query_ids: Optional set of query_id values to filter on.
        question_ids: Optional set of question no values to filter on.

    Returns:
        SpreadsheetDataset: The loaded dataset
    """
    data = await SpreadsheetDataset.from_gsheets(
        sheet_id="1bAcN8o43bRZABYTeNJ-DCIKSddwJIPW7jTWoNiJRTT8",
        worksheet_name="aip_data_analysis_agentv2",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )
    if query_ids:
        data = [r for r in data if int(r["query_id"]) in query_ids]
        print(f"Filtered to {len(data)} records by query_id={sorted(query_ids)}")
    if question_ids:
        data = [r for r in data if int(r["no"]) in question_ids]
        print(f"Filtered to {len(data)} records by question_id={sorted(question_ids)}")
    return data


if __name__ == "__main__":
    import asyncio

    dataset = asyncio.run(load_dataset())
    print(f"Loaded: {len(dataset)} data")
