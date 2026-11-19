# Google Sheets Experiment Tracker Tutorial

This tutorial demonstrates how to use the `GoogleSheetsExperimentTracker` with `evaluate_suites()` in the GenAI Evaluations SDK.

The `GoogleSheetsExperimentTracker` persists evaluation results directly in Google Sheets for easy sharing, collaborative viewing, and historical tracking, without requiring a dedicated backend service.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key
- A Google Cloud service account with the **Google Sheets API** and **Google Drive API** enabled
- Your target Google Sheet (or Drive folder) shared with the service account email as an **Editor**

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
# Edit .env with your API key and Google Sheets service account credentials
```

## Usage

Run the Google Sheets experiment tracker example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Google Sheets experiment tracker script
make clean      # Clean up generated files
```
