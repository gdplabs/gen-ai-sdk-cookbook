# Evaluate Helper Function Tutorials

The `evaluate()` helper function provides a streamlined way to run AI evaluations with minimal setup. It orchestrates the entire evaluation process, from data loading to result tracking, in a single function call.

## Tutorials

1. **[Standard Dataset Evaluation](evaluate_standard/)** — Using `evaluate()` with local CSV datasets.
2. **[Google Sheets Evaluation](evaluate_from_google_sheets/)** — Using `evaluate()` with Google Sheets as the data source.
3. **[Langfuse Experiment Tracker](evaluate_with_langfuse/)** — Using `evaluate()` with Langfuse tracking and custom column mapping.
4. **[Summary Evaluator](evaluate_with_summary/)** — Using `evaluate()` with custom summary evaluators for aggregate metrics.

## Function Signature

```python
async def evaluate(
    data: str | BaseDataset | list[EvalInput],
    evaluators: list[BaseEvaluator | BaseMetric],
    experiment_tracker: BaseExperimentTracker | None = None,
    batch_size: int = 10,
    allow_batch_evaluation: bool = False,
    summary_evaluators: list[SummaryEvaluatorCallable] | None = None,
    **kwargs: Any,
) -> ExperimentResult
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `str \| BaseDataset \| list[EvalInput]` | Dataset to evaluate |
| `evaluators` | `list[BaseEvaluator \| BaseMetric]` | Evaluators/metrics to apply |
| `experiment_tracker` | `BaseExperimentTracker \| None` | Optional tracker for logging results |
| `batch_size` | `int` | Number of samples to process in parallel (default: 10) |
| `allow_batch_evaluation` | `bool` | Enable batch processing mode for LLM API calls |
| `summary_evaluators` | `list[SummaryEvaluatorCallable] \| None` | Functions for computing aggregate metrics |

> **Note:** The `evaluate()` helper expects precomputed model outputs in your dataset (for example `actual_output`). It focuses only on evaluation and tracking, not on running inference.
