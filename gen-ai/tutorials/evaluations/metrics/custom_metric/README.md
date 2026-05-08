# Custom Metric Tutorial

This tutorial demonstrates how to create **custom metrics** in the GenAI Evaluations SDK when built-in metrics do not cover your evaluation need.

## Decision Flow

```
Do you need LLM judgment?
├── NO → Subclass BaseMetric (Approach 3)
│   Database checks, API validation, deterministic rules
│
└── YES → Is an existing metric close to what you need?
    ├── YES → Modify existing metric attributes
    │   Rubric, threshold, criteria, few-shot, evaluation_steps
    │   See [Modify Metrics](../modify_metrics)
    │
    └── NO → Do you need this across many datasets/projects?
        ├── YES → Subclass DeepEvalGEvalMetric (Approach 2)
        │   Reusable, class-based, import once
        │
        └── NO → DeepEvalGEvalMetric directly (Approach 1)
            Quick script, single-use prompt
```

## Approaches

### Approach 1: DeepEvalGEvalMetric Directly (Quick Custom Prompt)

**When:** you need a new quality dimension that no built-in metric covers, and it's a one-off evaluation — you don't expect to reuse the prompt across projects.

**Trade-off:** quick to write but tightly coupled to the script. If you need the same check in another project, you'll copy-paste.

**File:** `approach1_deepeval_geval_direct.py`

### Approach 2: Subclass DeepEvalGEvalMetric (Reusable LLM Judge)

**When:** the same custom quality dimension is evaluated across multiple datasets, projects, or evaluation runs. Subclassing gives you a reusable, importable metric class with the same `evaluate()` interface as built-in metrics.

Required components:

| Component | Description |
|-----------|-------------|
| `_defaults` | `MetricDefaults(name, criteria, rubric, evaluation_params, [evaluation_steps])` |
| `required_fields` | Set of `ColumnNames` fields the metric needs from input data |
| `input_type` | `LLMTestCase` (canonical input type) |
| `higher_is_better` | `True` or `False` — affects `MetricsAggregator` polarity inversion |
| `_to_rubric_score(raw)` | Convert normalized `[0,1]` back to native rubric integer |

**Files:** `approach2_politeness_metric.py`, `approach2_test_politeness.py`

### Approach 3: Subclass BaseMetric (Deterministic, No LLM)

**When:** the check doesn't need LLM judgment at all. Examples:
- "Did the agent create the order in the database?"
- "Is the response length under the maximum token limit?"
- "Does the output contain a valid JSON schema?"
- "Are all required environment variables set?"

No LLM call, no latency, no cost, deterministic result.

Required components:

| Component | Description |
|-----------|-------------|
| `name` | Metric key in evaluation output |
| `required_fields` | Set of field names from input data |
| `_evaluate(data)` | Async method returning `{score, explanation}` |

**Files:** `approach3_order_exists_metric.py`, `approach3_test_order_exists.py`

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key (for Approaches 1 and 2)

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API key
```

## Usage

Run each approach individually:

```bash
make run-approach1    # Quick custom prompt
make run-approach2    # Reusable LLM judge
make run-approach3    # Deterministic check (no LLM)
```

## Available Make Commands

```bash
make install         # Install dependencies using uv
make run-approach1   # Run Approach 1: DeepEvalGEvalMetric directly
make run-approach2   # Run Approach 2: Subclass DeepEvalGEvalMetric
make run-approach3   # Run Approach 3: Subclass BaseMetric
make clean           # Clean up generated files
```
