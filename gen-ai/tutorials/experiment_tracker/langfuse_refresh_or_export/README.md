# Langfuse Refresh or Export Tutorial

This tutorial demonstrates how to use the `LangfuseExperimentTracker` to refresh or export Langfuse session-level scores in the GenAI Evaluations SDK.

## Prerequisites

- Python 3.11 or higher
- Langfuse account and credentials

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
# Edit .env with your Langfuse credentials
```

## Usage

Run the refresh or export example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Langfuse refresh or export script
make clean      # Clean up generated files
```
