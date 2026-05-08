# Evaluate Helper Function

The `evaluate()` helper function provides a streamlined way to run AI evaluations with minimal setup. It orchestrates the entire evaluation process, from data loading to result tracking, in a single function call.

## Quick Start

### 1. Install Dependencies

```bash
make install
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the Examples

```bash
make run                # Run standard dataset evaluation
make run-google-sheets   # Run Google Sheets evaluation
make run-langfuse        # Run evaluation with Langfuse tracking
make run-summary         # Run evaluation with summary evaluator
```

## Examples

### Example 1: Standard Dataset Evaluation

**Run:** `make run`

**File:** [evaluate_standard.py](evaluate_standard.py)

This example demonstrates using `evaluate()` with standard datasets (local files or built-in datasets).

```python
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator

results = await evaluate(
    data=DictDataset.from_csv("dataset_examples/simple_qa_data.csv"),
    evaluators=[GEvalGenerationEvaluator()],
)
```

**Features:**
- Local CSV dataset loader
- Precomputed outputs in LLMTestCase format
- CSV experiment tracker

### Example 2: Google Sheets Evaluation

**Run:** `make run-google-sheets`

**File:** [evaluate_from_google_sheets.py](evaluate_from_google_sheets.py)

This example demonstrates using `evaluate()` with Google Sheets as the data source.

```python
from gllm_evals import LLMTestCase
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from inference_mock import your_ai_func_result

dataset = (
    await SpreadsheetDataset.from_gsheets(
        sheet_id="YOUR_SHEET_ID",
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )
).to_standard_format()

data = [
    LLMTestCase(
        input=row["input"],
        actual_output=your_ai_func_result(row["input"])["actual output"],
        expected_output=row["expected_output"],
        retrieved_context=your_ai_func_result(row["input"])["retrieved_context"],
    )
    for row in dataset
]

results = await evaluate(
    data=data,
    evaluators=[GEvalGenerationEvaluator()],
)
```

**Prerequisites:**
- Google Sheets API credentials in `.env`:
  - `GOOGLE_SHEETS_CLIENT_EMAIL`
  - `GOOGLE_SHEETS_PRIVATE_KEY`

### Example 3: Langfuse Experiment Tracker with Custom Mapping

**Run:** `make run-langfuse`

**File:** [evaluate_with_langfuse.py](evaluate_with_langfuse.py)

This example demonstrates using `evaluate()` with Langfuse experiment tracking and custom column mapping.

```python
from langfuse import get_client
from gllm_evals import LLMTestCase
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker
from inference_mock import your_ai_func_result

mapping = {
    "input": {
        "question_id": "question_id",
        "query": "input",
        "retrieved_context": "retrieved_context",
        "generated_response": "generated_output",
    },
    "expected_output": {"expected_response": "expected_output"},
    "metadata": {"topic": "topic"},
}

dataset = (
    await SpreadsheetDataset.from_gsheets(
        sheet_id="YOUR_SHEET_ID",
        worksheet_name="test_dataset",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )
).to_standard_format()

data = [
    LLMTestCase(
        input=row["input"],
        actual_output=your_ai_func_result(row["input"])["actual output"],
        expected_output=row["expected_output"],
        retrieved_context=your_ai_func_result(row["input"])["retrieved_context"],
    )
    for row in dataset
]

results = await evaluate(
    data=data,
    evaluators=[GEvalGenerationEvaluator()],
    experiment_tracker=LangfuseExperimentTracker(
        langfuse_client=get_client(),
        mapping=mapping,
    ),
)
```

**Prerequisites:**
- Google Sheets API credentials in `.env`
- Langfuse credentials in `.env`:
  - `LANGFUSE_PUBLIC_KEY`
  - `LANGFUSE_SECRET_KEY`

### Example 4: Summary Evaluator

**Run:** `make run-summary`

**File:** [evaluate_with_summary.py](evaluate_with_summary.py)

This example demonstrates using `evaluate()` with custom summary evaluators for aggregate metrics.

```python
import json

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.types import EvaluatorResult, MetricInput
from inference_mock import your_ai_func_result


def accuracy_summary(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, float]:
    """Compute average accuracy from evaluation results."""
    weighted_average_list = []
    for row_results in evaluation_results:
        evaluation_result = next(result for result in row_results if "generation" in result)
        generation_result = evaluation_result["generation"]
        weighted_average = (
            generation_result["completeness"]["score"]
            + generation_result["redundancy"]["score"] * 3
        ) / 2
        weighted_average_list.append(weighted_average)
    return {"weighted_average": sum(weighted_average_list) / len(weighted_average_list)}


def counter_aggregator(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, float]:
    """Count the number of evaluated rows."""
    return {"counter": len(evaluation_results)}


data = [
    LLMTestCase(
        input=row["query"],
        actual_output=your_ai_func_result(row["query"])["actual output"],
        expected_output=row["expected_response"],
        retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
    )
    for row in DictDataset.from_csv("dataset_examples/simple_qa_data.csv").load()
]

result = await evaluate(
    data=data,
    evaluators=[GEvalGenerationEvaluator(metrics=[GEvalCompletenessMetric(), GEvalRedundancyMetric()])],
    summary_evaluators=[accuracy_summary, counter_aggregator],
    batch_size=1,
)

print(json.dumps(result, indent=2))
```

## Understanding the `evaluate()` Function

### Function Signature

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

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `str \| BaseDataset \| list[EvalInput]` | Dataset to evaluate. Can be a `BaseDataset` object, a string path, or a list of `LLMTestCase` rows |
| `evaluators` | `list[BaseEvaluator \| BaseMetric]` | Evaluators/metrics to apply |
| `experiment_tracker` | `BaseExperimentTracker \| None` | Optional tracker for logging results. Defaults to `SimpleExperimentTracker` |
| `batch_size` | `int` | Number of samples to process in parallel (default: 10) |
| `allow_batch_evaluation` | `bool` | Enable batch processing mode for LLM API calls |
| `summary_evaluators` | `list[SummaryEvaluatorCallable] \| None` | Functions for computing aggregate metrics across all results |

## Data Sources

The `data` parameter supports multiple formats:

```python
# HuggingFace Hub
data="hf/[dataset_name]"

# Google Sheets
data="gs/[worksheet_name]"

# Langfuse dataset
data="langfuse/[dataset_name]"

# Local file (CSV or JSONL)
data="[dataset_name]"

# Built-in dataset
data=load_simple_qa_dataset()

# List of LLMTestCase objects (precomputed outputs)
data=[
    LLMTestCase(
        input=row["query"],
        actual_output=row["actual_output"],
        expected_output=row["expected_response"],
        retrieved_context=row["retrieved_context"],
    )
    for row in dataset
]
```

> **Note:** The `evaluate()` helper expects precomputed model outputs in your dataset (for example `actual_output`). It focuses only on evaluation and tracking, not on running inference.

### Required Keys per Test Case

For `GEvalGenerationEvaluator`, each `LLMTestCase` should contain:
- `actual_output` (required) — the model-generated response to evaluate
- `expected_output` (optional) — ground truth for comparison
- `retrieved_context` (optional) — for RAG evaluations

## Output Format

```json
{
  "experiment_uris": {
    "run_uri": "/path/to/experiments/experiment_results.csv",
    "leaderboard_uri": "/path/to/experiments/leaderboard.csv"
  },
  "run_id": "default_simple_qa_data_55d8ad1d",
  "dataset_name": "simple_qa_data",
  "timestamp": "2026-01-31T10:34:05.930843",
  "num_samples": 4,
  "metadata": {
    "batch_size": 10,
    "evaluator_parameters": { ... }
  },
  "summary_result": {}
}
```

## Summary Evaluators

Compute aggregate metrics across all evaluation results:

```python
def accuracy_summary(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, float]:
    """Compute average accuracy from evaluation results."""
    weighted_average_list = []
    for row_results in evaluation_results:
        evaluation_result = next(result for result in row_results if "generation" in result)
        generation_result = evaluation_result["generation"]
        weighted_average = (
            generation_result["completeness"]["score"]
            + generation_result["redundancy"]["score"] * 3
        ) / 2
        weighted_average_list.append(weighted_average)
    return {"weighted_average": sum(weighted_average_list) / len(weighted_average_list)}
```

## Experiment Tracking

### Langfuse Integration

```python
from langfuse import get_client
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import (
    LangfuseExperimentTracker,
)

mapping = {
    "input": {
        "question_id": "question_id",
        "query": "input",
        "retrieved_context": "retrieved_context",
        "generated_response": "generated_output"
    },
    "expected_output": {
        "expected_response": "expected_output"
    },
    "metadata": {
        "topic": "topic"
    }
}

results = await evaluate(
    data=...,
    evaluators=[...],
    experiment_tracker=LangfuseExperimentTracker(
        langfuse_client=get_client(),
        mapping=mapping,
    ),
)
```

## Available Make Commands

```bash
make install              # Install dependencies
make run                  # Run standard dataset evaluation
make run-google-sheets     # Run Google Sheets evaluation
make run-langfuse          # Run evaluation with Langfuse tracking
make run-summary           # Run evaluation with summary evaluator
make clean                 # Clean up generated files
```
