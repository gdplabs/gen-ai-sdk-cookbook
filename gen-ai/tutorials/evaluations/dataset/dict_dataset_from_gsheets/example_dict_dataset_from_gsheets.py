"""Example of loading a dataset from Google Sheets using DictDataset.

Authors:
    Mikhael Chris (mikhael.chris@gdplabs.id)

References:
    NONE
"""

import asyncio
import os

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset


async def main():
    """Main function."""
    raw_dataset = await DictDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )

    data = [
        LLMTestCase(
            input=row.get("input"),
            actual_output=row.get("generated_output"),
            expected_output=row.get("expected_output"),
            retrieved_context=row.get("retrieved_context"),
        )
        for row in raw_dataset.load()
    ]

    print(data)


if __name__ == "__main__":
    asyncio.run(main())
