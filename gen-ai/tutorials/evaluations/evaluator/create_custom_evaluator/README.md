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
make run                # Run custom_evaluator.py (CompositeEvaluator with built-in metrics)
make run-extend         # Run extend_evaluator.py (subclass BaseEvaluator)
make run-short-circuit  # Run short_circuit_evaluator.py (subclass BaseEvaluator, fail fast)
```

## Two Approaches to Custom Evaluators

### Approach 1: Combine Built-in Metrics with CompositeEvaluator

**Run:** `make run`

The easiest way to build your own evaluator is to combine any set of built-in metrics in a `CompositeEvaluator`. It runs the metrics and aggregates their results for you.

```python
from gllm_evals import LLMTestCase
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalAnswerRelevancyMetric,
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
)

evaluator = CompositeEvaluator(
    metrics=[GEvalCompletenessMetric(), GEvalGroundednessMetric(), DeepEvalAnswerRelevancyMetric()],
    name="generation_quality",
)
result = await evaluator.evaluate(
    LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital city of France.",
        expected_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France."],
    )
)
```

**Use this approach when:**
- You can use existing metrics
- You want to mix and match built-in metrics
- You need a simple solution

### Approach 2: Extend BaseEvaluator

**Run:** `make run-extend`

For customized evaluation logic, extend `BaseEvaluator` and implement `_evaluate()`. It receives an `LLMTestCase` and returns an `EvaluatorResult`, a dict that maps each metric name to its result. A custom metric extends `BaseMetric` and returns a `MetricScore`.

```python
from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import EvaluatorResult, LLMTestCase, MetricScore


class ExactMatchMetric(BaseMetric):
    def __init__(self) -> None:
        super().__init__()
        self.name = "exact_match"

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        score = int(data.actual_output == data.expected_output)
        return MetricScore(score=score, explanation=None)


class ResponseEvaluator(BaseEvaluator):
    def __init__(self) -> None:
        super().__init__(name="response_evaluator")
        self.metric = ExactMatchMetric()

    async def _evaluate(self, data: LLMTestCase) -> EvaluatorResult:
        return {self.metric.name: await self.metric.evaluate(data)}
```

`short_circuit_evaluator.py` (`make run-short-circuit`) shows another `BaseEvaluator` subclass. It runs its metrics in order and stops at the first metric that fails, so later metrics are not run.

**Use this approach when:**
- You need customized evaluation logic, such as a fixed order or early stop
- Built-in metrics don't fit your use case
- You have specific scoring requirements

## Built-in Metrics

Some built-in metrics that you can combine in a `CompositeEvaluator`:

| Category | Metrics |
|----------|---------|
| **Generation** | `GEvalCompletenessMetric`, `GEvalGroundednessMetric`, `GEvalRedundancyMetric` |
| **Answer Relevance** | `DeepEvalAnswerRelevancyMetric` |
| **Retrieval** | `DeepEvalContextualPrecisionMetric`, `DeepEvalContextualRecallMetric`, `GEvalContextSufficiencyMetric` |
| **Custom** | Create your own by extending `BaseMetric` |

## Example Output

`evaluate()` returns a dict that maps the evaluator name to an `EvaluatorOutput`. For `make run-extend`:

```text
{'response_evaluator': EvaluatorOutput(error=None, aggregate_success=True, aggregate_score=1.0, aggregate_explanation='All metrics met the expected values.', evaluator_token_usage=None, exact_match=MetricResult(score=1, explanation=None, error=None, rubric_score=1, success=True, threshold=0.5, strict_mode=False, higher_is_better=True, token_usage=None, decision=None, model_id=None))}
```

Each metric result is an extra field of `EvaluatorOutput` (here `exact_match`), next to the aggregate fields.

## Data Types

All evaluators and metrics take an `LLMTestCase` (or a list of them) as input.

## Available Make Commands

```bash
make install            # Install dependencies
make run                # Run custom_evaluator.py
make run-extend         # Run extend_evaluator.py
make run-short-circuit  # Run short_circuit_evaluator.py
make clean              # Clean up generated files
```

## Next Steps

- [Multiple LLM-as-a-Judge](../../multiple_llm_as_a_judge/) - Use multiple judges for better alignment
- [Evaluate Suites](../../evaluate_suites/) - Run evaluators over one or more datasets with `evaluate_suites()`
