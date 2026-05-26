import asyncio
import os

from gllm_evals import LLMTestCase, evaluate
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from gllm_evals.types import (
    GoogleDriveAttachmentConfig,
    LocalAttachmentConfig,
    S3AttachmentConfig,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def example_local_attachments():
    """Example: Load attachments from a local directory."""
    config = LocalAttachmentConfig(
        local_directory="./example_images",
    )
    dataset = SpreadsheetDataset.from_csv(
        data_path="dataset_with_attachments.csv",
        attachments_config=config,
    )
    data = dataset.load()
    data = [
        LLMTestCase(
            input=row.get("input"),
            actual_output=row.get("actual_output"),
            expected_output=row.get("expected_output", ""),
        )
        for row in data
    ]
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=model)],
        experiment_tracker=CSVExperimentTracker(project_name="local_attachments_example"),
    )
    print(f"Local attachments: {results['run_id']}")


async def example_s3_attachments():
    """Example: Load attachments from an S3 bucket."""
    config = S3AttachmentConfig(
        s3_bucket=os.getenv("S3_BUCKET", "your-bucket"),
        s3_prefix="attachments/",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_region=os.getenv("AWS_REGION", "ap-southeast-3"),
    )
    dataset = SpreadsheetDataset.from_csv(
        data_path="dataset_with_s3_attachments.csv",
        attachments_config=config,
    )
    data = dataset.load()
    data = [
        LLMTestCase(
            input=row.get("input"),
            actual_output=row.get("actual_output"),
        )
        for row in data
    ]
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=model)],
        experiment_tracker=CSVExperimentTracker(project_name="s3_attachments_example"),
    )
    print(f"S3 attachments: {results['run_id']}")


async def example_gdrive_attachments():
    """Example: Load attachments from Google Drive."""
    config = GoogleDriveAttachmentConfig(
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
        folder_id="your-folder-id",
    )
    dataset = SpreadsheetDataset.from_csv(
        data_path="dataset_with_gdrive_attachments.csv",
        attachments_config=config,
    )
    data = dataset.load()
    data = [
        LLMTestCase(
            input=row.get("input"),
            actual_output=row.get("actual_output"),
        )
        for row in data
    ]
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    results = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=model)],
        experiment_tracker=CSVExperimentTracker(project_name="gdrive_attachments_example"),
    )
    print(f"Google Drive attachments: {results['run_id']}")


async def main():
    """Demonstrate all three attachment loading approaches."""
    await example_local_attachments()
    await example_s3_attachments()
    await example_gdrive_attachments()


if __name__ == "__main__":
    asyncio.run(main())
