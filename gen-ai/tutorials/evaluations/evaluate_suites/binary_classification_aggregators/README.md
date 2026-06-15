# Evaluate Suites — Binary Classification Aggregators (TPR / TNR)

This example demonstrates **`true_positive_rate`** and **`true_negative_rate`** run aggregators for binary classification evaluation.

Given a dataset where each row is labelled `"TRUE"` (positive) or `"FALSE"` (negative), these aggregators measure how well an evaluator identifies each class:

| Metric | Measures | Equation |
|---|---|---|
| **TPR** (Sensitivity) | How well the evaluator **accepts** correct responses | TP / (TP + FN) |
| **TNR** (Specificity) | How well the evaluator **rejects** incorrect responses | TN / (TN + FP) |

Rows where the evaluator did not produce a result are excluded from both numerator and denominator.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- Google AI API Key

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

## How the label field works

The `label` field on `LLMTestCase` determines the ground truth:

```python
# Positive test case
LLMTestCase(
    input="What is the capital of France?",
    actual_output="Paris is the capital of France.",
    expected_output="Paris",
    label="TRUE",          # ← this response should be accepted
)

# Negative test case
LLMTestCase(
    input="What is the capital of France?",
    actual_output="France has many beautiful cities.",
    expected_output="Paris",
    label="FALSE",         # ← this response should be rejected
)
```

The label can be:
- `"TRUE"` / `"true"` / `True` — positive class
- `"FALSE"` / `"false"` / `False` — negative class
- `None` — excluded from TPR/TNR computation

## Using with evaluate_suites

Run aggregators also work with `evaluate_suites()`, running per-suite and pooled:

```python
result = await evaluate_suites(
    suites=[suite_1, suite_2],
    run_aggregators=[true_positive_rate, true_negative_rate],
)
```

The built-in `summary_accuracy` is always prepended automatically.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the binary classification example
make clean      # Clean up generated files
```

## Reference

- [Run Aggregators Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/run-aggregators)
- [Evaluate Suites Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluate-suites)
