import asyncio
import os

from gllm_evals.dataset.dict_dataset import DictDataset


async def main():
    """Main function."""
    # Map the sheet's generated_output column to the LLMTestCase actual_output field.
    dataset = await DictDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
        field_mapping={"generated_output": "actual_output"},
    )
    data = dataset.load()

    print(data)


if __name__ == "__main__":
    asyncio.run(main())
