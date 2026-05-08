# DictDataset from CSV Tutorial

This tutorial demonstrates how to load a dataset from a CSV file using `DictDataset` in the GenAI Evaluations SDK.

The simple QA CSV uses domain-specific column names. This example shows how to remap them to the canonical field names expected by evaluators before evaluation.

## Prerequisites

- Python 3.11 or higher

## Installation

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

## Usage

Run the CSV dataset example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the CSV dataset script
make clean      # Clean up generated files
```
