# Evaluate Suites — Standard Example

This example demonstrates **`evaluate_suites()`** with three suites using built-in datasets from `gllm-evals`:

| Suite | Dataset Source | Evaluator | Focus |
|---|---|---|---|
| **qa** | `load_simple_qa_dataset()` | `GEvalGenerationEvaluator` | Completeness, groundedness, redundancy |
| **rag** | `load_simple_rag_dataset()` | `CompositeEvaluator` with `GEvalGroundednessMetric` | Retrieved-context groundedness |
| **agent** | `load_simple_agent_tool_call_dataset()` | `AgentEvaluator` | Tool-call correctness + generation quality |

## How It Works

| Step | Description |
|---|---|
| 1 | Each suite pulls data from a library built-in dataset, mapping columns to `LLMTestCase` fields |
| 2 | Suites are defined explicitly in code (one per use case) with their own evaluator |
| 3 | `evaluate_suites()` runs all suites with a shared `run_id` and experiment tracker |
| 4 | Results are printed as JSON |

### Evaluator details

- **qa** — `GEvalGenerationEvaluator` measures completeness (did the answer cover the key facts?), groundedness (is the answer supported by context?), and redundancy (is the answer concise?).
- **rag** — Composite evaluator focused on retrieved-context groundedness only.
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

## Adding a new suite

Add a new `EvalSuite` in `evaluate_suites_standard.py`:

```python
new_suite = EvalSuite(
    name="your_suite",
    data=[_to_eval_row(r) for r in load_your_dataset().load()],
    evaluators=[YourEvaluator(models=[judge_model])],
)
result = await evaluate_suites(
    suites=[qa_suite, rag_suite, agent_suite, new_suite],
    ...
)
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites script
make clean      # Clean up generated files
```
