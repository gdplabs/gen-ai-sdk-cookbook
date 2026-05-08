# Evaluator Tutorial

This tutorial demonstrates how to use the **Evaluator** in the GenAI Evaluator SDK.

An Evaluator orchestrates evaluation workflows by coordinating metrics and evaluation logic. All evaluators inherit from `BaseEvaluator` and share a common aggregation layer:

- Executes relevant metrics (parallel or sequential)
- Aggregates results via `MetricsAggregator` — computes `aggregate_success` (AND-gate: all metrics must pass) and `aggregate_score` (polarity-aware mean)
- Generates human-readable `aggregate_explanation`

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key (or OpenAI API Key)

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

## Input & Output Types

Evaluators accept either dictionaries or `LLMTestCase` objects as input data.

Example `LLMTestCase`:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris",
    actual_output="New York",
    retrieved_context="Paris is the capital of France.",
)
```

While Evaluator outputs an `EvaluatorResult` that includes keys such as `aggregate_explanation`, `score`, and namespaced metrics result.

## Single vs Batch Evaluation

### Single Evaluation

Evaluate a single test case:

```python
result: EvaluatorResult = await evaluator.evaluate(data)
```

### Batch Evaluation

Evaluate multiple test cases at once:

```python
results: list[EvaluatorResult] = await evaluator.evaluate([data1, data2, data3])
```

## Available Evaluators

1. `GEvalGenerationEvaluator`
2. `AgentEvaluator`
3. `ClassicalRetrievalEvaluator`
4. `LMBasedRetrievalEvaluator`
5. `QueryTransformerEvaluator`
6. `SummarizationEvaluator`
7. `CompositeEvaluator`

Looking for something else? Build your own custom evaluator in the [Custom Evaluator tutorial](../create_custom_evaluator_scorer/).

## Usage

Run the single evaluation example:

```bash
make run-single
```

Run the batch evaluation example:

```bash
make run-batch
```

## Available Make Commands

```bash
make install       # Install dependencies using uv
make run-single    # Run the single evaluation script
make run-batch     # Run the batch evaluation script
make clean         # Clean up generated files
```
