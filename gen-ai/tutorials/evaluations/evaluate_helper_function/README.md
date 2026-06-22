# Evaluate Suites Tutorials

The `evaluate_suites()` function provides a streamlined way to run AI evaluations with minimal setup. It orchestrates the entire evaluation process, from data loading to result tracking, in a single function call.

## Tutorials

1. **[Standard Dataset Evaluation](evaluate_standard/)** — Using `evaluate_suites()` with local CSV datasets.
2. **[Google Sheets Evaluation](evaluate_from_google_sheets/)** — Using `evaluate_suites()` with Google Sheets as the data source.
3. **[Langfuse Experiment Tracker](evaluate_with_langfuse/)** — Using `evaluate_suites()` with Langfuse tracking and custom column mapping.
4. **[Summary Evaluator](evaluate_with_summary/)** — Using `evaluate_suites()` with custom summary evaluators for aggregate metrics.

## Function Signature

```python
async def evaluate_suites(
    suites: list[EvalSuite],
    experiment_tracker: BaseExperimentTracker | None = None,
    batch_size: int = 10,
    run_aggregators: list[AggregatorCallable] | None = None,
) -> ExperimentResult
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `suites` | `list[EvalSuite]` | List of evaluation suites to run |
| `experiment_tracker` | `BaseExperimentTracker \| None` | Optional tracker for logging results |
| `batch_size` | `int` | Number of samples to process in parallel (default: 10) |
| `run_aggregators` | `list[AggregatorCallable] \| None` | Functions for computing aggregate metrics |

Each `EvalSuite` wraps a dataset and its evaluators:

```python
EvalSuite(
    data=list[EvalInput],
    evaluators=list[BaseEvaluator | BaseMetric],
    name=str | None,  # optional suite name
)
```

> **Note:** `evaluate_suites()` expects precomputed model outputs in your dataset (for example `actual_output`). It focuses only on evaluation and tracking, not on running inference.
