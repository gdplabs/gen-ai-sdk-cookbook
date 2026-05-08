# DictDataset from Langfuse Tutorial

This tutorial demonstrates how to load a dataset from Langfuse using `DictDataset` (read-only) in the GenAI Evaluations SDK.

Langfuse stores dataset item inputs as structured objects (dicts), so the `input` field may be a dict rather than a plain string. This example shows how to extract the relevant key that matches your dataset schema (e.g. `query`) before passing to `LLMTestCase`.

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

Run the Langfuse dataset example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Langfuse dataset script
make clean      # Clean up generated files
```
