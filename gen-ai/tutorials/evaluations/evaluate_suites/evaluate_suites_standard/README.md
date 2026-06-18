# Evaluate Suites — Standard Example

This example demonstrates **`evaluate_suites()`** with two suites using local data files:

| Suite | Data Source | Evaluator | Focus |
|---|---|---|---|
| **qa** | `data/simple_qa_data.csv` | `GEvalGenerationEvaluator` | Completeness, groundedness, redundancy |
| **agent** | `data/simple_agent_tool_call_data.json` | `AgentEvaluator` | Tool-call correctness + generation quality |

## How It Works

| Step | Description |
|---|---|
| 1 | Each suite loads test cases from a local data file |
| 2 | Suites are defined explicitly in code with their own evaluator |
| 3 | `evaluate_suites()` runs all suites with a shared `run_id` |
| 4 | Results are printed as JSON |

### Evaluator details

- **qa** — `GEvalGenerationEvaluator` measures completeness (did the answer cover the key facts?), groundedness (is the answer supported by context?), and redundancy (is the answer concise?).
- **agent** — `AgentEvaluator` measures both the response quality and the correctness of tool calls (`tools_called` vs `expected_tools`).

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
- A Google AI API Key

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
# Edit .env with your Google API key
```

## Usage

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites script
make clean      # Clean up generated files
```
