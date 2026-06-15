# Evaluate Suites — Binary Classification Aggregators (TPR / TNR)

This example demonstrates **`evaluate_suites()`** with binary classification run aggregators (**TPR** and **TNR**).

Test cases are loaded from a CSV dataset with a `category` field. Each category becomes
its own `EvalSuite` automatically — no need to define suites one by one.

## Dataset

The CSV in `data/eval_dataset.csv` uses column names consistent with the library's built-in
datasets (`simple_qa_data.csv`, `simple_rag_data.csv` from `gllm-evals/examples/sample_data/`),
with additional `category` and `label` columns:

| Column | Source | Description |
|--------|--------|-------------|
| `question_id` | Library convention | Row identifier |
| `category` | Added | Suite name — rows with the same value form one `EvalSuite` |
| `label` | Added | `TRUE` (positive) or `FALSE` (negative) for TPR/TNR |
| `query` | Library convention | The user query |
| `generated_response` | Library convention | Your system's response |
| `expected_response` | Library convention | The ideal / ground-truth response |
| `retrieved_context` | Library convention | Retrieved documents (required for groundedness metrics) |

## How It Works

### Data flow

| Step | Description |
|------|-------------|
| 1 | `data/eval_dataset.csv` contains all test cases with `category` and `label` columns |
| 2 | `DictDataset.from_csv()` loads the CSV as a flat list of dicts |
| 3 | Rows are grouped by `category` into `standard_rag` and `agent_qna` |
| 4 | One `EvalSuite` is built per category with category-specific evaluators |
| 5 | `evaluate_suites()` runs all suites and computes TPR / TNR / accuracy |

### Binary classification metrics

| Metric | Measures | Equation | Scope |
|--------|----------|----------|-------|
| **TPR** (Sensitivity) | How well the evaluator **accepts** correct responses | TP / (TP + FN) | Only `label="TRUE"` rows |
| **TNR** (Specificity) | How well the evaluator **rejects** incorrect responses | TN / (TN + FP) | Only `label="FALSE"` rows |
| **Accuracy** | Overall pass rate | passed / total | All rows |

The built-in `summary_accuracy` is always prepended automatically by `evaluate_suites()`.

### Evaluator mapping

The `category_evaluators` dict in `main()` maps each category to its evaluators:

- **`standard_rag`** — `GEvalGroundednessMetric` + `GEvalCompletenessMetric`
- **`agent_qna`** — `GEvalCompletenessMetric` + `GEvalRedundancyMetric`

Adding a new category is just one new row in the CSV + one entry in the dict.

### Experiment tracker

This example uses `CSVExperimentTracker` explicitly (the Google Sheets tracker
has known compatibility issues with run aggregators).

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
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

## Expected output

```json
{
  "run_aggregators_result": {
    "accuracy": {
      "groundedness": 0.8,
      "generation": 0.6
    },
    "true_positive_rate": {
      "groundedness": 1.0,
      "generation": 1.0
    },
    "true_negative_rate": {
      "groundedness": 0.5,
      "generation": 1.0
    }
  }
}
```

## Adding new test cases

Open `data/eval_dataset.csv` and add a row:

```csv
11,standard_rag,TRUE,"What is the capital of France?","Paris is the capital of France.","Paris","France is a country in Europe. Paris is the capital."
```

No code changes needed — the script groups by `category` automatically.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the example
make clean      # Clean up generated files
```

## Reference

- [Evaluate Suites Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluate-suites)
- [Run Aggregators Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/run-aggregators)
