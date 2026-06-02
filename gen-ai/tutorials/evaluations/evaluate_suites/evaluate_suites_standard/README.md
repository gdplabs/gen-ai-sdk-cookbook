# Evaluate Suites — Standard Example

This example demonstrates **`evaluate_suites()`** with test cases loaded from a CSV file. Each row has a `suite` column that determines which `EvalSuite` the test case belongs to.

You can add, remove, or reorganise test cases across suites by editing the CSV alone — no code changes needed.

## How It Works

| File | Purpose |
|---|---|
| `data/eval_dataset.csv` | All test cases with a `suite` column for grouping |
| `evaluate_suites_standard.py` | Loads CSV, groups by `suite`, builds one `EvalSuite` per group, runs `evaluate_suites()` |

### CSV columns

| Column | Required | Description |
|---|---|---|
| `suite` | Yes | Suite name — rows with the same value go to the same `EvalSuite` |
| `input` | Yes | The user query |
| `actual_output` | Yes | Your system's response |
| `expected_output` | Yes | The ideal / ground-truth response |
| `retrieved_context` | No | Retrieved documents (required for groundedness metrics) |

### Evaluator mapping

The `_evaluators()` function in `main()` maps each suite name to its evaluators. In this example:

- **`qa`** / **`general`** — `GEvalGenerationEvaluator` (completeness, redundancy, etc.)
- **`rag`** — `CompositeEvaluator` with `GEvalGroundednessMetric`

Add new suite names to `_evaluators()` when you add them to the CSV.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google AI API Key

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
# Edit .env with your Google API key
```

## Usage

```bash
make run
```

## Adding Test Cases

Open `data/eval_dataset.csv` and add a new row:

```csv
suite,input,actual_output,expected_output,retrieved_context
qa,"What is the capital of Indonesia?","Jakarta is the capital of Indonesia.","Jakarta","Indonesia is a country in Southeast Asia. Jakarta is the capital city."
```

No code changes needed — the script groups rows by `suite` automatically.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites script
make clean      # Clean up generated files
```
