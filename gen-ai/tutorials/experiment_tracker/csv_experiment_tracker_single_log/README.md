# CSV Experiment Tracker Single Log Tutorial

This tutorial demonstrates how to use the `CSVExperimentTracker` to log a single evaluation result manually in the GenAI Evaluations SDK.

Unlike the full evaluation example, this script directly constructs an evaluation result dict and logs it without running an evaluator.

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

Run the CSV experiment tracker single log example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the CSV experiment tracker single log script
make clean      # Clean up generated files
```
