# DictDataset from HuggingFace Hub Tutorial

This tutorial demonstrates how to load a dataset from HuggingFace Hub using `DictDataset` in the GenAI Evaluations SDK.

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

Run the HuggingFace Hub dataset example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the HuggingFace Hub dataset script
make clean      # Clean up generated files
```
