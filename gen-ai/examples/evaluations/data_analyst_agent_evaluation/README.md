# Integration Test Suite for aip_data_analysis_agent

This directory contains pytest-based integration tests for the aip_data_analysis_agent benchmark.

## Quick Start

### Prerequisites
Set the following environment variables:

```bash
export AIP_BASE_URL="https://your-aip-server"
export AIP_API_KEY="your-api-key"
export GOOGLE_API_KEY="your-google-api-key"         # For evaluation model (Gemini)

# LM config for ephemeral agent creation
export LM_MODEL_ID="your-model-id"                  # e.g. "gpt-4o-mini"
export OAI_COMPATIBLE_BEARER_TOKEN="your-lm-key"    # Bearer token for the LM API
export OAI_COMPATIBLE_BASE_URL="https://your-lm-api" # Base URL of the OAI-compatible LM
```

### Run Tests

```bash
# Run all tests with verbose output
pytest benchmarks/aip_data_analysis_agent/eval/ -v

# Run a specific test class
pytest benchmarks/aip_data_analysis_agent/eval/test_evaluation.py::TestQuestion001 -v

# Run with extended output and capture disabled
pytest benchmarks/aip_data_analysis_agent/eval/ -vv -s
```

## Structure

- **`questions.py`** — Hardcoded question definitions (5 PoC questions based on investment analysis domain)
- **`metrics.py`** — Metric helpers:
  - `keyword_match()` — Check if response contains all required keywords
  - `completeness_score()` — LLM-based completeness evaluation (1–3 scale)
- **`conftest.py`** — Pytest configuration:
  - `aip_client` — Session-scoped AIP client fixture
  - `lm_invoker` — Session-scoped language model invoker (Google Gemini)
  - `csv_results` — Session-scoped result accumulator
  - `pytest_runtest_logreport()` — Logs test results after each test
  - `pytest_sessionfinish()` — Writes CSV results at session end
- **`test_evaluation.py`** — Test classes (one per question):
  - `TestQuestion001` through `TestQuestion005`
  - Each class has:
    - `response` fixture (invokes agent once per class)
    - `test_response_not_empty()` — Checks response is not empty
    - `test_keyword_match()` — Validates keywords
    - `test_completeness()` — Checks LLM-based completeness score ≥ 2

## Output

Test results are written to: **`benchmarks/aip_data_analysis_agent/eval/results/results.csv`**

CSV format:
```
question_id, query, expected_response, pass_fail, tests_passed, tests_total
q001, "What are the top 5 companies...", "...", PASS, 3, 3
...
```

## Design Notes

- **PoC**: Concise and simple, no over-engineering
- **Direct pytest invocation**: Not invoked via `benchmark.sh`
- **One class per question**: Isolated test namespaces, easy to extend
- **Session-scoped fixtures**: Efficient client reuse; agent invoked once per question
- **Ephemeral agents**: Agents are created on the AIP server at session start (with unique suffixed names) and deleted at session end — no persistent state left on the server
- **CSV logging**: Simple output for analysis and tracking
