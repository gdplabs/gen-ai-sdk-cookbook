# CSV Experiment Tracker Tutorial

This tutorial shows how to record evaluator results with `CSVExperimentTracker` in the GenAI Evaluations SDK.

The `CSVExperimentTracker` logs evaluation results to CSV files, enabling local experiment tracking and analysis.

## Prerequisites

- Python 3.12 or higher
- An OpenRouter API Key for the default judge model

## Installation

### 1. Install Dependencies

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
pip install gllm-evals-binary
```

### 2. Set Up Environment Variables

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
