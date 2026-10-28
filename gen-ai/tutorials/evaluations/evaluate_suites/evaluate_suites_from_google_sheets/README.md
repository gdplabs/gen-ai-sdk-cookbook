# Evaluate Suites — Google Sheets as the Data Source

This tutorial shows how to use **`evaluate_suites()`** with Google Sheets as the data source in the GenAI Evaluator SDK.

The script loads rows from a Google Sheet with `SpreadsheetDataset.from_gsheets()`. It adds mock outputs from `inference_mock.py` and evaluates the rows as one `EvalSuite`.

To write the evaluation results to Google Sheets instead, see [Evaluate Suites — Google Sheets Experiment Tracker](../evaluate_suites_with_google_sheets_experiment_tracker/).

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
- An OpenRouter API Key for the DeepSeek judge model
- Google Sheets API enabled with service account credentials

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install Dependencies

```bash
make install
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your OpenRouter API key and Google Sheets credentials
```

`GOOGLE_SHEETS_PRIVATE_KEY` must be the Base64-encoded `private_key` of your service account. A raw PEM key causes a credential error. To encode the key from the service account JSON file:

```bash
jq -r .private_key service-account.json | base64 | tr -d '\n'
```

### 4. Prepare Your Google Sheet

1. Create a Google Sheet with a worksheet named `test_dataset`.
2. Download [data/test_dataset.csv](data/test_dataset.csv) from this tutorial.
3. In Google Sheets, select **File > Import > Upload** and upload the CSV file.
4. Select **Replace current sheet** as the import location.
5. Share the sheet with your service account email (`GOOGLE_SHEETS_CLIENT_EMAIL`) as **Viewer**.
6. Copy the sheet ID from its URL, `https://docs.google.com/spreadsheets/d/<sheet ID>/edit`.
7. Set `GOOGLE_SHEETS_SHEET_ID` in `.env` to this ID.

Keep the `input` values unchanged. The mock accepts only the two questions in this file.
To use other questions, update the sheet rows and `inference_mock.py` together.

## Input & Output Types

Each `EvalSuite` accepts `LLMTestCase` objects as input data.

Example `LLMTestCase`:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the Capital of France?",
    expected_output="Paris",
    actual_output="New York",
    retrieved_context="Paris is the capital of France.",
)
```

`evaluate_suites()` returns a `SuiteExperimentResult` with the results of each suite under `suites`.

## Usage

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites from Google Sheets script
make clean      # Clean up generated files
```
