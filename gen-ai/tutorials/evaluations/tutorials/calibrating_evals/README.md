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
```

## Examples

### Example 1: Standard Dataset Evaluation

**Run:** `make run`

**File:** [evaluate_standard.py](evaluate_standard.py)

This example demonstrates using `evaluate()` with standard datasets (local files or built-in datasets).

```python
from gllm_evals import load_simple_qa_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator

results = await evaluate(
    data=load_simple_qa_dataset('.dataset_examples'),
    inference_fn=inference_fn,
    evaluators=[
        GEvalGenerationEvaluator(
            model_credentials=os.getenv("GOOGLE_API_KEY")
        )
    ],
)
```

**Features:**
- Built-in dataset loader
- Default inference function
- Custom inference function option

### Example 2: Google Sheets Evaluation

**Run:** `make run-google-sheets`

**File:** [evaluate_from_google_sheets.py](evaluate_from_google_sheets.py)

This example demonstrates using `evaluate()` with Google Sheets as the data source, including Langfuse experiment tracking.

```python
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker

mapping = {
    "input": {
        "question_id": "question_id",
        "query": "query",
        "retrieved_context": "retrieved_context",
        "generated_response": "generated_response",
    },
    "expected_output": {"expected_response": "expected_response"},
    "metadata": {"topic": "topic"},
}

results = await evaluate(
    data=await SpreadsheetDataset.from_gsheets(
        sheet_id="YOUR_SHEET_ID",
        worksheet_name="test",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    ),
    inference_fn=inference_fn,
    evaluators=[GEvalGenerationEvaluator(...)],
    experiment_tracker=LangfuseExperimentTracker(
        langfuse_client=get_client(),
        mapping=mapping,
    ),
)
```

**Prerequisites:**
- Google Sheets API credentials in `.env`:
  - `GOOGLE_SHEETS_CLIENT_EMAIL`
  - `GOOGLE_SHEETS_PRIVATE_KEY`
- Langfuse credentials (optional, for experiment tracking):
  - `LANGFUSE_PUBLIC_KEY`
  - `LANGFUSE_SECRET_KEY`

## Understanding the `evaluate()` Function

### Function Signature

```python
async def evaluate(
    data: str | BaseDataset,
    inference_fn: Callable,
    evaluators: list[BaseEvaluator | BaseMetric],
    experiment_tracker: BaseExperimentTracker | None = None,
    batch_size: int = 10,
    allow_batch_evaluation: bool = False,
    summary_evaluators: list[SummaryEvaluatorCallable] | None = None,
    **kwargs: Any,
) -> list[list[EvaluationOutput]]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `str \| BaseDataset` | Dataset to evaluate. Can be a `BaseDataset` object or a string path |
| `inference_fn` | `Callable` | Function that generates responses to be evaluated |
| `evaluators` | `list[BaseEvaluator \| BaseMetric]` | Evaluators/metrics to apply |
| `experiment_tracker` | `BaseExperimentTracker \| None` | Optional tracker for logging results |
| `batch_size` | `int` | Number of samples to process in parallel (default: 10) |
| `allow_batch_evaluation` | `bool` | Enable batch processing mode for LLM API calls |
| `summary_evaluators` | `list[Callable]` | Functions for computing aggregate metrics |

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
```

## Inference Function Requirements

Your `inference_fn` must accept a `row` parameter (dictionary) and return a dictionary with the evaluation keys:

```python
def generate_response(row: dict[str, Any]) -> dict[str, Any]:
    query = row["user_query"]
    # Your inference logic
    generated_response = run_something(query)
    return {"generated_response": generated_response}
```

### Required Keys

The evaluation keys must match exactly what the evaluator expects. For `GEvalGenerationEvaluator`:
- `generated_response` (required)

### Optional Keys

You may include additional keys:
- `retrieved_context` - For RAG evaluations

## Output Format

```json
{
  "experiment_urls": {
    "run_url": "/path/to/experiments/experiment_results.csv",
    "leaderboard_url": "/path/to/experiments/leaderboard.csv"
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
    evaluation_results: list[EvaluationOutput],
    data: list[MetricInput]
) -> dict[str, float]:
    """Compute average accuracy from evaluation results."""
    weighted_average_list = []
    for evaluation_result in evaluation_results:
        generation_result = evaluation_result["generation"]
        weighted_average = (
            generation_result["completeness"]["score"]
            + generation_result["redundancy"]["score"] * 3
        ) / 2
        weighted_average_list.append(weighted_average)
    return {"weighted_average": sum(weighted_average_list) / len(weighted_average_list)}

# Usage
result = await evaluate(
    data=load_simple_qa_dataset(),
    inference_fn=inference_fn,
    evaluators=[GEvalGenerationEvaluator(...)],
    summary_evaluators=[accuracy_summary],
)
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
        "query": "query",
        "retrieved_context": "retrieved_context",
        "generated_response": "generated_response"
    },
    "expected_output": {
        "expected_response": "expected_response"
    },
    "metadata": {
        "topic": "topic"
    }
}

results = await evaluate(
    data=...,
    inference_fn=inference_fn,
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
make clean                # Clean up generated files
```
