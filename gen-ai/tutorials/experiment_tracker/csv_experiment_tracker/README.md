# CSV Experiment Tracker Tutorial

This tutorial demonstrates how to use the `CSVExperimentTracker` with the `evaluate` function in the GenAI Evaluations SDK.

The `CSVExperimentTracker` logs evaluation results to CSV files, enabling local experiment tracking and analysis.

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

Run the CSV experiment tracker example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the CSV experiment tracker script
make clean      # Clean up generated files
```
