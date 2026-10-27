# Evaluate Suites — Custom Run Aggregator

This tutorial shows how to write a **custom run aggregator** and pass it to **`evaluate_suites()`**.

A run aggregator is a function that receives the evaluation results of all rows in a run and returns run-level values. `evaluate_suites()` adds these values to `run_aggregators_result`, next to the results of the built-in aggregators (for example `accuracy`). For the built-in `true_positive_rate` and `true_negative_rate` aggregators, see [Evaluate Suites — Binary Classification](../evaluate_suites_binary_classification/).

The example aggregator, `weighted_quality`, gives one score per run from two metrics of `GEvalGenerationEvaluator`:

```text
row score = (completeness + 3 * (1 - redundancy)) / 4
```

Both scores are normalized to [0, 1]. Completeness is higher-is-better and redundancy is lower-is-better, so the formula uses `1 - redundancy`.

## Aggregator Signature

```python
def weighted_quality(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[LLMTestCase],
) -> dict[str, Any]: ...
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `evaluation_results` | `list[list[EvaluatorResult]]` | One list per row, parallel to `data`. Each `EvaluatorResult` maps an evaluator name to an `EvaluatorOutput`. |
| `data` | `list[LLMTestCase]` | The input rows of the run. |
| **Returns** | `dict[str, Any]` | Values to add to `run_aggregators_result`. |

`EvaluatorOutput` is a pydantic model. Its per-metric results are extra fields, so read them from `model_extra`:

```python
completeness = output.model_extra["completeness"].score
```

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
- An OpenRouter API Key for the default judge model

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
# Edit .env with your OpenRouter API key
```

## Usage

```bash
make run
```

The script prints `run_aggregators_result`:

```json
{
  "accuracy": {
    "generation": 1.0
  },
  "weighted_quality": 1.0
}
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites custom run aggregator script
make clean      # Clean up generated files
```
