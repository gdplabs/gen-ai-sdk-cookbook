# Evaluate Suites — Binary Classification Aggregators (TPR / TNR)

This example demonstrates **`evaluate_suites()`** with binary classification run aggregators (**TPR** and **TNR**).

Test cases are loaded from a JSON dataset with a `category` field. Each category becomes
its own `EvalSuite` automatically — no need to define suites one by one.

## Dataset

The JSON in `data/eval_dataset.json` uses these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `question_id` | Yes | Row identifier |
| `category` | Yes | Suite name — rows with the same value form one `EvalSuite` |
| `label` | Yes | `true` (positive) or `false` (negative) for TPR/TNR |
| `query` | Yes | The user query |
| `generated_response` | Yes | Your system's response |
| `expected_response` | Yes | The ideal / ground-truth response |
| `retrieved_context` | No | Retrieved documents (required for groundedness metrics) |
| `tools_called` | No | Tools invoked by your system (for `agent_qna` suite) |
| `expected_tools` | No | Expected tools (for `agent_qna` suite) |

## How It Works

### Data flow

| Step | Description |
|------|-------------|
| 1 | `data/eval_dataset.json` contains all test cases with `category` and `label` fields |
| 2 | `json.loads()` loads the JSON as a flat list of dicts |
| 3 | Rows are grouped by `category` into `standard_rag` and `agent_qna` |
| 4 | One `EvalSuite` is built per category with category-specific evaluators |
| 5 | `evaluate_suites()` runs all suites and computes TPR / TNR |

### Binary classification metrics

| Metric | Measures | Equation | Scope |
|--------|----------|----------|-------|
| **TPR** (Sensitivity) | How well the evaluator **accepts** correct responses | TP / (TP + FN) | Only `label=true` rows |
| **TNR** (Specificity) | How well the evaluator **rejects** incorrect responses | TN / (TN + FP) | Only `label=false` rows |
| **Accuracy** | Overall pass rate | passed / total | All rows |

The built-in `summary_accuracy` is always prepended automatically by `evaluate_suites()`.

### Evaluator mapping

The `category_evaluators` dict in `main()` maps each category to its evaluators:

- **`standard_rag`** — `GEvalGenerationEvaluator` with `GEvalCompletenessMetric` + `GEvalGroundednessMetric`
- **`agent_qna`** — `AgentEvaluator`

Adding a new category is just one new entry in the JSON + one entry in the dict.

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

## Adding new test cases

Open `data/eval_dataset.json` and add an entry with the appropriate `category` and `label`.

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
