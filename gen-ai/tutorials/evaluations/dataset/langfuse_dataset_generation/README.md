# Langfuse Dataset Generation Tutorial

This tutorial demonstrates how to generate and upload a dataset to Langfuse, then evaluate it using the GenAI Evaluations SDK.

The example loads a local CSV dataset, uploads it to Langfuse as a dataset, converts it to `LLMTestCase` format, and runs a `GEvalGenerationEvaluator` for quality assessment.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key
- Langfuse account and credentials

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
# Edit .env with your API keys
```

## Input & Output Types

The `GEvalGenerationEvaluator` accepts `LLMTestCase` objects with the following fields:

- `input` (str) — The user question.
- `actual_output` (str) — The model's output to be evaluated.
- `expected_output` (str, optional) — The reference or ground truth answer.
- `retrieved_context` (str, optional) — The supporting context used during generation.

## Usage

Run the Langfuse dataset generation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Langfuse dataset generation script
make clean      # Clean up generated files
```
