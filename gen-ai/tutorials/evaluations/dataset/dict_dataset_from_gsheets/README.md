# DictDataset from Google Sheets Tutorial

This tutorial demonstrates how to load a dataset from Google Sheets using `DictDataset` in the GenAI Evaluations SDK.

## Prerequisites

- Python 3.11 or higher
- A Google Cloud service account with access to Google Sheets API
- Service account `client_email` and `private_key`

## Installation

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

### Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your Google Sheets service account credentials
```

## Usage

Run the Google Sheets dataset example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Google Sheets dataset script
make clean      # Clean up generated files
```
