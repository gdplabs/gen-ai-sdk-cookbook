# Evaluate Suites — Google Sheets as the Data Source

This tutorial shows how to use **`evaluate_suites()`** with Google Sheets as the data source in the GenAI Evaluator SDK.

The script loads the rows from a Google Sheet with `SpreadsheetDataset.from_gsheets()`, adds the output of your AI system to each row (`inference_mock.py` gives a mock output), and evaluates the rows as one `EvalSuite`.

To write the evaluation results to Google Sheets instead, see [Evaluate Suites — Google Sheets Experiment Tracker](../evaluate_suites_with_google_sheets_experiment_tracker/).

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
- An OpenRouter API Key for the default judge model
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

The service account must have read access to the Google Sheet.

## Input & Output Types

Each `EvalSuite` accepts `LLMTestCase` objects as input data.

Example `LLMTestCase`:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
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
