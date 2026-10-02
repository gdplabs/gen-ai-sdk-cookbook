# JSON Experiment Tracker Tutorial

This tutorial demonstrates how to use the `JSONExperimentTracker` with the `evaluate` function in the GenAI Evaluations SDK.

The `JSONExperimentTracker` is a lightweight, local tracker like `CSVExperimentTracker`, but `get_run_results()` returns the real `LLMTestCase` and `EvaluatorResult` objects it was given, instead of values re-parsed from a CSV row.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key

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
# Edit .env with your API key
```

## Usage

Run the JSON experiment tracker example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the JSON experiment tracker script
make clean      # Clean up generated files
```
