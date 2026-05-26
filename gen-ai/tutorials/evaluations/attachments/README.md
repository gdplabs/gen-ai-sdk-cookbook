# Tutorial: Using Attachments with GenAI Evaluations SDK

This tutorial demonstrates how to load and use attachments (images, audio, documents) for multi-modal evaluation with the GenAI Evaluations SDK.

## Supported Attachment Sources

| Source | Config Class | Use Case |
|--------|-------------|----------|
| Local Directory | `LocalAttachmentConfig` | Attachments stored on your local filesystem |
| Amazon S3 | `S3AttachmentConfig` | Attachments stored in an S3 bucket |
| Google Drive | `GoogleDriveAttachmentConfig` | Attachments stored in Google Drive |

## Setup

1. Install dependencies:
   ```bash
   make install
   ```

2. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. Run the example:
   ```bash
   make run
   ```

## How It Works

The `attachments_config` parameter on dataset loaders (e.g., `SpreadsheetDataset.from_csv()`, `DictDataset`) tells the SDK where to find attachments referenced in your dataset rows.

The dataset CSV/Google Sheet should contain an `attachments` column with filenames that match the files at the attachment source.

## Example

```python
from gllm_evals.types import LocalAttachmentConfig
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset

config = LocalAttachmentConfig(local_directory="./images/")
dataset = SpreadsheetDataset.from_csv(
    data_path="my_dataset.csv",
    attachments_config=config,
)
```
