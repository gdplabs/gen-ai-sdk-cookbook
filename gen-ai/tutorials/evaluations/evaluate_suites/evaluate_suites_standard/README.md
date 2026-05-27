# Evaluate Suites — Standard Example

This example demonstrates the basic usage of the **`evaluate_suites()`** helper function in the GenAI Evaluator SDK.

The `evaluate_suites()` function allows you to evaluate multiple data partitions (suites) with different evaluators under a single experiment — sharing one `run_id` and one experiment tracker.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- An OpenAI API Key

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install Dependencies

```bash
make install
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Usage

Run the multi-suite evaluation:

```bash
make run
```

## What's Happening

This example creates **three evaluation suites**:

1. **`qa`** — 2 general knowledge questions, evaluated with `GEvalGenerationEvaluator`
2. **`rag`** — 2 context-based questions, evaluated with `CompositeEvaluator(groundedness)`
3. **`suite_0`** (auto-named) — 1 arithmetic question, evaluated with `GEvalGenerationEvaluator`

All three suites share:
- One `run_id`
- One `CSVExperimentTracker`
- Base dataset name: `multi_suite_evaluation`

Each suite's results are accessible via `result.suites["qa"]`, `result.suites["rag"]`, etc. Pooled metrics combining all suites are at `result.run_aggregators_result`.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites script
make clean      # Clean up generated files
```
