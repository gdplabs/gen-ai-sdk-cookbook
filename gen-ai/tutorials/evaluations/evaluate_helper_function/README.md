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
    experiment_tracker: type[BaseExperimentTracker] | BaseExperimentTracker | None = None,
    batch_size: int = 10,
    allow_batch_evaluation: bool = False,
    run_aggregators: list[RunAggregatorCallable] | None = None,
    dataset_name: str | None = None,
    run_id: str | None = None,
    **kwargs: Any,
) -> SuiteExperimentResult
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `suites` | `list[EvalSuite]` | List of evaluation suites to run |
| `experiment_tracker` | `type[BaseExperimentTracker] \| BaseExperimentTracker \| None` | Tracker class, instance, or `None` (defaults to CSV) |
| `batch_size` | `int` | Number of samples per batch (default: 10) |
| `allow_batch_evaluation` | `bool` | Enable batch processing for LLM API calls (default: `False`) |
| `run_aggregators` | `list[RunAggregatorCallable] \| None` | Functions for computing aggregate metrics |
| `dataset_name` | `str \| None` | Base dataset name; auto-generated with timestamp if not provided |
| `run_id` | `str \| None` | Shared run ID across all suites; auto-generated if not provided |

Each `EvalSuite` wraps a dataset and its evaluators:

```python
EvalSuite(
    data=str | BaseDataset | list[EvalInput],
    evaluators=list[BaseEvaluator],
    name=str | None,  # optional suite name, auto-generated as suite_0, suite_1, ... if not set
)
```

> **Note:** `evaluate_suites()` expects precomputed model outputs in your dataset (for example `actual_output`). It focuses only on evaluation and tracking, not on running inference.
