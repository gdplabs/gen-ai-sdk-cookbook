# Composite Evaluator Tutorial

This tutorial demonstrates how to use the **CompositeEvaluator** in the GenAI Evaluator SDK.

The `CompositeEvaluator` runs multiple metrics in parallel or sequential mode and aggregates their results into a unified evaluation report. It follows the GoF Composite design pattern, treating multiple metrics as a single evaluator unit.

## When to Use Composite Evaluator

Use `CompositeEvaluator` when you need to:

- **Run multiple metrics together** — Evaluate your model using several metrics at once
- **Control execution mode** — Choose between parallel (faster) or sequential (ordered) execution
- **Aggregate results** — Get a unified report with aggregate scores and success indicators
- **Combine different metric types** — Mix metrics from different categories (Generation, Retrieval, Safety, Tool Use)
- **Orchestrate metrics without a built-in evaluator** — When no pre-built evaluator exists for your specific combination of metrics, use CompositeEvaluator to orchestrate them yourself

## How It Works

The `CompositeEvaluator`:

1. **Accepts a list of metrics** — Any `BaseMetric` objects can be composed together
2. **Executes metrics** — Runs them in parallel (default) or sequentially
3. **Merges results** — Combines all metric outputs into a single result dictionary
4. **Aggregates scores** — Uses `MetricsAggregator` for polarity-aware binary scoring
5. **Returns unified output** — Provides `aggregate_success` and `aggregate_score` alongside individual metric results

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

## Basic Example

```python
import asyncio
from gllm_evals import LLMTestCase
from gllm_evals.dataset import load_simple_rag_dataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalContextualPrecisionMetric,
    DeepEvalContextualRecallMetric,
)

async def main():
    # Create metrics using existing implementations
    contextual_recall = DeepEvalContextualRecallMetric()
    contextual_precision = DeepEvalContextualPrecisionMetric()

    # Create composite evaluator
    evaluator = CompositeEvaluator(
        metrics=[contextual_recall, contextual_precision],
        name="deepeval_contextual_evaluator",
    )

    # Load test data
    raw = load_simple_rag_dataset()
    data = [
        LLMTestCase(
            input=row.input,
            actual_output=row.actual_output,
            expected_output=row.expected_output,
            retrieved_context=row.retrieved_context,
        )
        for row in raw.load()
    ]

    # Evaluate
    result = await evaluator.evaluate(data[0])
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```json
{
  "deepeval_contextual_evaluator": {
    "aggregate_explanation": "All metrics met the expected values.",
    "aggregate_success": true,
    "aggregate_score": 0.95,
    "contextual_recall": {
      "score": 1.0,
      "explanation": "The retrieved context contains all relevant information...",
      "rubric_score": 1.0,
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "contextual_precision": {
      "score": 0.9,
      "explanation": "Most retrieved context is relevant...",
      "rubric_score": 0.9,
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    }
  }
}
```

## Advanced: Custom Aggregation

You can provide a custom `MetricsAggregator` for polarity-aware binary scoring:

```python
from gllm_evals.aggregation.metrics_aggregator import MetricsAggregator

custom_aggregator = MetricsAggregator(
    # Custom aggregation logic
)

evaluator = CompositeEvaluator(
    metrics=[metric1, metric2],
    name="custom_aggregation_eval",
    parallel=True,
    metrics_aggregator=custom_aggregator,
)
```

## Fault Isolation

If one metric fails, `CompositeEvaluator` continues evaluating the remaining metrics. The failed metric's error is captured in the results, but other metrics still execute.

If instead you want short-circuit behavior — stop on first failure and skip the rest — this requires subclassing `BaseEvaluator` directly. See [Create Custom Evaluator / Scorer](../create_custom_evaluator_scorer/) for the pattern.

## Usage

Run the composite evaluation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the composite evaluation script
make clean      # Clean up generated files
```
