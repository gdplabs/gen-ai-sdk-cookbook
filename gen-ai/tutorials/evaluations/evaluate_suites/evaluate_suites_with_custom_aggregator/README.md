# Evaluate Suites — Custom Run Aggregators

This example demonstrates how to use **`evaluate_suites()`** with **custom run aggregators**.

Run aggregators are callables that receive `(evaluation_results, data)` and return a `dict` of computed metrics. They are applied per-suite and pooled across all suites, letting you define custom aggregate statistics alongside the built-in `summary_accuracy`.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- Google AI API Key

## Installation

```bash
make install
```

### Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your Google API key
```

## Usage

```bash
make run
```

## Custom Aggregator

The example defines `weighted_average_score`, which extracts every evaluator's `aggregate_score` across all rows and suites, then computes their mean:

```python
def weighted_average_score(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, float]:
    scores = []
    for row_results in evaluation_results:
        for result in row_results:
            for eval_data in result.values():
                if isinstance(eval_data, dict) and "aggregate_score" in eval_data:
                    scores.append(eval_data["aggregate_score"])
    return {"weighted_average": sum(scores) / len(scores)}
```

The `run_aggregators` parameter is passed to `evaluate_suites()`. The built-in `summary_accuracy` is always prepended automatically.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites with custom aggregator script
make clean      # Clean up generated files
```
