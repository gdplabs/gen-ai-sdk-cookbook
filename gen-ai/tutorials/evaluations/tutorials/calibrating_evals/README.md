# Calibrating Evals

This tutorial walks through iteratively calibrating an LLM judge until it agrees with your SMEs on both good and bad outputs. The target metric is **TPR ≥ 90% and TNR ≥ 90%**.

See the full tutorial: [Calibrating Your Evals](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/calibrate-the-evals/)

## Iterations

| Script | What changes |
|--------|-------------|
| `evaluate.py` | Baseline — single evaluator, no category split |
| `evaluate-iter1.py` | Category-split suites: composite evaluator for `context_sufficiency`, lenient groundedness for `groundedness_2` |
| `evaluate-iter2.py` | Adds custom rubric + few-shot for context sufficiency, multi-judge voting for `default-multijudge` |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- `gcloud` CLI authenticated (`gcloud auth login`)
- Access to the `gen-ai-internal` package index

## Setup

### 1. Install dependencies

```bash
make install
```

This creates a `.venv`, authenticates to the internal index via `gcloud`, and syncs all packages.

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Running

```bash
make run        # Baseline evaluation
make run-iter1  # Iteration 1: category-split suites
make run-iter2  # Iteration 2: custom rubric + multi-judge
```

Each run outputs a JSON result with per-suite scores and aggregated TPR/TNR to stdout, and writes CSV experiment results to `calibration/`.

## Make Commands

```bash
make help       # List all commands
make install    # Install dependencies
make run        # Baseline evaluation
make run-iter1  # Iteration 1
make run-iter2  # Iteration 2
make clean      # Remove __pycache__, *.pyc, experiments/
```

## Project Structure

```
calibrating_evals/
├── data/
│   └── dataset.csv          # 15 labeled test cases (label: TRUE/FALSE)
├── evaluate.py              # Baseline: single GEval evaluator
├── evaluate-iter1.py        # Iter 1: category-split EvalSuites
├── evaluate-iter2.py        # Iter 2: custom rubric, multi-judge
├── pyproject.toml
├── Makefile
└── .env.example
```

## Dataset

The dataset covers a **cruise market analysis agent**: 15 test cases mixing factual lookups, open-ended synthesis, and inference-heavy analysis. Each row has a `category` field that drives which suite it belongs to, and a `label` field (`TRUE`/`FALSE`) that TPR/TNR aggregation reads.

[View dataset →](https://docs.google.com/spreadsheets/d/1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M/edit?gid=1585438283#gid=1585438283)
