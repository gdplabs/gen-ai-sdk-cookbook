# Integration Test Suite for aip_data_analysis_agent

This directory contains pytest-based integration tests for the aip_data_analysis_agent benchmark.

## Quick Start

### Prerequisites
Set the following environment variables:

```bash

export GOOGLE_API_KEY="your-google-api-key"         # For evaluation model (Gemini)
export GOOGLE_SHEETS_CLIENT_EMAIL="your-google-sheets-client-email" # For loading dataset from Google Sheets
export GOOGLE_SHEETS_PRIVATE_KEY="your-google-sheets-private-key" # For loading dataset from Google Sheets
```

### Run Tests

```bash
# Run all tests with verbose output
pytest evaluations/ -v

# Run specific test function
pytest evaluations/test_evaluate_agent.py::test_standard_case -v

# Run specific test case by ID (format: q{query_id}_no_{question_number})
pytest evaluations/test_evaluate_agent.py::test_standard_case[q1_no_48] -v

# Run multiple specific test cases using -k flag (keyword matching)
pytest evaluations/ -k "no_48 or no_64" -v

# Run all test cases for a specific query ID
pytest evaluations/ -k "q1_" -v

# Run all test cases for specific question numbers across all tests
pytest evaluations/ -k "no_48 or no_64 or no_88" -v

# Run with extended output and capture disabled
pytest evaluations/ -vv -s
```

**Note:** Test IDs follow the format `q{query_id}_no_{question_number}` (e.g., `q1_no_48` means query_id=1, question number=48). Use the `-k` flag for flexible filtering by keywords.

### Using Makefile

Convenient make targets are available for common test operations:

```bash
# Run all tests
make test

# Run with verbose output
make test-verbose

# See what tests would be collected (without running)
make test-collect

# Run specific test cases by keyword
make test-keyword KEYWORD="no_48 or no_64"
make test-keyword KEYWORD="q1_"
make test-keyword KEYWORD="test_standard_case"
```

## Structure

- **`questions.py`** — Async dataset loader from Google Sheets
- **`metrics/`** — Metric implementations:
  - `completeness.py` — LLM-based completeness evaluation (1–3 scale)
  - `resolution_rate.py` — Chart validation with custom assertions
  - `deterministic.py` — Basic deterministic checks (has_answer)
- **`conftest.py`** — Pytest configuration and utilities:
  - `get_dataset()` — Loads and caches dataset from Google Sheets
  - `filter_data()` — Filters dataset by query_id/question_id for parametrization
  - `result_collector` — Session-scoped fixture for collecting test results
  - `pytest_sessionfinish()` — Writes CSV results at session end
- **`evaluations/`** — Test files and evaluator:
  - `agent_evaluator.py` — AgentEvaluator class with metric methods
  - `test_evaluate_agent.py` — Parametrized tests using explicit data filtering

## Output

Test results are written to: **`benchmarks/aip_data_analysis_agent/eval/results/results.csv`**

CSV format:
```
question_id, query, expected_response, pass_fail, tests_passed, tests_total
q001, "What are the top 5 companies...", "...", PASS, 3, 3
...
```

## Writing Custom Tests

The evaluation suite provides a simple, explicit pattern for test parametrization using standard `@pytest.mark.parametrize`:

```python
import pytest
from conftest import get_dataset, filter_data
from evaluations.agent_evaluator import AgentEvaluator

# Load and filter data at module level
test_cases, test_ids = filter_data(get_dataset(), query_ids=[1, 2, 3])

# Use standard pytest.mark.parametrize with the filtered data
@pytest.mark.parametrize("record", test_cases, ids=test_ids)
def test_my_evaluation(record: dict) -> None:
    evaluator = AgentEvaluator(query_id=int(record["query_id"]))
    
    # Run metrics
    has_answer = evaluator.metric_has_answer(record)
    completeness = evaluator.metric_completeness_score(record)
    
    # Assert results
    assert has_answer is True
    assert completeness >= 3.0
```

### Key Functions

- **`get_dataset()`**: Loads dataset from Google Sheets on first call, then caches it. Use this for explicit parametrization at module level.
- **`filter_data(data, query_ids, question_ids)`**: Filters dataset and returns `(cases, ids)` tuple for parametrize.

### Filtering Options

```python
# Filter by query IDs
cases, ids = filter_data(get_dataset(), query_ids=[1, 2, 3])

# Filter by question numbers
cases, ids = filter_data(get_dataset(), question_ids=[10, 20, 30])

# Filter by both
cases, ids = filter_data(get_dataset(), query_ids=17, question_ids=[1, 2])

# No filter - all data
cases, ids = filter_data(get_dataset())
```

### Important Notes

- **Filtering in code, not CLI**: All data filtering is done explicitly in test files using `filter_data()`. This makes the test data selection transparent and visible in the code.
- **Data loads once**: The dataset is loaded on first call to `get_dataset()` and cached for the entire test session.

## Design Notes

- **User-oriented**: Test files explicitly show what data they test using standard `@pytest.mark.parametrize`
- **Plugin-ready**: No magic hooks, follows standard pytest patterns
- **Async loading, sync access**: Dataset loads from Google Sheets asynchronously on first call, then cached
- **Flexible filtering**: Easy to create custom test combinations using `filter_data()`
- **Transparent**: All data selection happens in test code, not via CLI magic
- **CSV logging**: Results exported to `results/history_eval_results.csv`
