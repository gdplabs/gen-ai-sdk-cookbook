# Create Custom Evaluator / Scorer

If the built-in evaluators don't cover your use case, you can define your own! This tutorial demonstrates two main ways to create a custom evaluator.

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
make run        # Run custom_evaluator.py (Extending BaseEvaluator)
make run-extend # Run extend_evaluator.py (Combining Built-in Metrics)
```

## Two Approaches to Custom Evaluators

### Approach 1: Extend BaseEvaluator

**Run:** `make run`

For highly customized evaluation logic, create your own class by extending `BaseEvaluator` and defining your evaluation logic from scratch.

```python
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.evaluator.evaluator import BaseEvaluator

class ExactMatchMetric(BaseMetric):
    def __init__(self):
        self.name = "exact_match"

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        score = int(data["generated_response"] == data["expected_response"])
        return {"score": score}

class ResponseEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__(name="response_evaluator")
        self.metric = ExactMatchMetric()

    async def _evaluate(self, data: MetricInput) -> EvaluationOutput:
        return await self.metric.evaluate(data)
```

**Use this approach when:**
- You need highly customized evaluation logic
- Built-in metrics don't fit your use case
- You have specific scoring requirements

### Approach 2: Use CustomEvaluator

**Run:** `make run-extend`

The easiest way to build your own evaluator is by combining any set of metrics into a `CustomEvaluator`.

```python
from gllm_evals.evaluator.custom_evaluator import CustomEvaluator
from gllm_evals.metrics.retrieval.ragas_context_precision import RagasContextPrecisionWithoutReference
from gllm_evals.metrics.retrieval.ragas_context_recall import RagasContextRecall

evaluator = CustomEvaluator(
    metrics=[ragas_context_recall, ragas_context_precision],
    name="my_evaluator",
)
```

**Use this approach when:**
- You can use existing metrics
- You want to mix and match built-in metrics
- You need a simple solution

## Built-in Metrics

The SDK provides many built-in metrics you can use with `CustomEvaluator`:

| Category | Metrics |
|----------|---------|
| **Retrieval** | `RagasContextRecall`, `RagasContextPrecisionWithoutReference`, `RagasFaithfulness` |
| **Generation** | `GEvalGenerationEvaluator` (completeness, groundedness, redundancy, etc.) |
| **Answer Relevance** | `AnswerRelevancyMetric` |
| **Custom** | Create your own by extending `BaseMetric` |

## Example Output

### Custom Evaluator (BaseEvaluator)

```json
{
  "response_evaluator": {
    "global_explanation": "All metrics met the expected values.",
    "exact_match": {
      "score": 1
    }
  }
}
```

### Custom Evaluator with Metrics

```json
{
  "my_evaluator": {
    "factual_correctness": {
      "score": 1.0,
      "explanation": null
    },
    "context_recall": {
      "score": 1.0,
      "explanation": null
    }
  }
}
```

## Data Types

Different evaluators require different data types:

| Data Type | Description |
|-----------|-------------|
| `QAData` | For question-answering evaluations |
| `RAGData` | For RAG pipeline evaluations |
| `MetricInput` | Generic dictionary input for custom metrics |

## Available Make Commands

```bash
make install    # Install dependencies
make run        # Run custom_evaluator.py
make run-extend # Run extend_evaluator.py
make clean      # Clean up generated files
```

## Next Steps

- [Multiple LLM-as-a-Judge](../multiple_llm_as_a_judge/) - Use multiple judges for better alignment
- [Evaluate Helper Function](../evaluate_helper_function/) - Use the convenience function
