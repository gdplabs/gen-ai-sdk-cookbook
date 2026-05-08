# Google Sheets Evaluation Tutorial

This tutorial demonstrates how to use the **`evaluate()`** helper function with Google Sheets as the data source in the GenAI Evaluator SDK.

The `evaluate()` function provides a streamlined way to run AI evaluations with minimal setup. It orchestrates the entire evaluation process, from data loading to result tracking, in a single function call.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key (or OpenAI API Key)
- Google Sheets API credentials

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys and Google Sheets credentials
```

## Input & Output Types

The `evaluate()` helper accepts `LLMTestCase` objects as input data.

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

## Usage

Run the Google Sheets evaluation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Google Sheets evaluation script
make clean      # Clean up generated files
```
