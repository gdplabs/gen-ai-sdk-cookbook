# Multiple LLM-as-a-Judge

Multiple LLM-as-a-Judge is an advanced evaluation approach that uses multiple language models as judges to evaluate tasks in parallel and aggregate their results using ensemble methods. This approach provides higher alignment with human judgment and can significantly accelerate human annotation workflows.

## Key Benefits

1. **Higher Alignment**: Multiple judges provide more reliable and consistent evaluations compared to single-judge approaches.
2. **Faster Human Annotation**: Humans can focus on scoring only cases where agreement score < 100%, reducing annotation workload.
3. **Human Alignment**: When agreement score reaches 100%, the alignment with human judgment is high.

Use multiple LLM-as-a-Judge when judge results are inconsistent or when you find disagreement between different LLM judge models.

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
make run-homogeneous    # Run homogeneous judge example
make run-heterogeneous  # Run heterogeneous judge example
```

## Usage

### Homogeneous Judges (Same Model)

Use the same model instantiated multiple times as judges.

**Run:** `make run-homogeneous`

**File:** [homogeneous_judge_example.py](homogeneous_judge_example.py)

```python
import asyncio
import os

from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.constant import AggregationMethod
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase


async def main() -> None:
    model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    evaluator = GEvalGenerationEvaluator(
        models=[model] * 3,
        aggregation_method=AggregationMethod.MAJORITY_VOTE,
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris",
        retrieved_context="Paris is the capital of France.",
    )
    result = await evaluator.evaluate(data)
    print(result)
```

### Heterogeneous Judges (Different Models)

Use different models as judges for broader perspective.

**Run:** `make run-heterogeneous`

**File:** [heterogeneous_judge_example.py](heterogeneous_judge_example.py)

```python
import asyncio
import os

from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.constant import AggregationMethod
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase


async def main() -> None:
    judges = [
        build_lm_invoker("openai/gpt-4o", os.getenv("OPENAI_API_KEY")),
        build_lm_invoker("openai/gpt-4o-mini", os.getenv("OPENAI_API_KEY")),
    ]
    evaluator = GEvalGenerationEvaluator(
        models=judges,
        aggregation_method=AggregationMethod.MAJORITY_VOTE,
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris",
        retrieved_context="Paris is the capital of France.",
    )
    result = await evaluator.evaluate(data)
    print(result)
```

## Output Shape

When only one model is set in `models`, each metric returns a normal single-judge result without ensemble metadata.

When multiple judges are set in `models`, metric-level results include ensemble metadata:

| Field | Description |
|-------|-------------|
| `score` | Aggregated metric score |
| `agreement_score` | Judge agreement in `[0.0, 1.0]` |
| `individual_judge_results` | Raw result from each judge, including judge error payloads if a judge fails |
| `ensemble_method` | Aggregation method actually used |
| `num_judges` | Total judges used |
| `representative_judge_index` | Judge result selected as representative for explanation fields |
| `explanation_aggregation_method` | Strategy used for combining or selecting explanations |
| `score_distribution` | Count of each score value |

Each item in `individual_judge_results` can include:

- `judge_id`
- `model_id`
- `score`
- `explanation`
- `rubric_score`
- `success`
- `threshold`
- `strict_mode`
- `higher_is_better`

If a judge fails, its item can contain `error`, `judge_id`, and `model_id` instead of score fields.

At evaluator aggregate level, ensemble output uses aggregate fields:

| Field | Description |
|-------|-------------|
| `aggregate_score` | Aggregated evaluator score |
| `aggregate_success` | Majority pass/fail result across valid judges |
| `aggregate_explanation` | Combined judge aggregate explanations, labeled by judge model |
| `agreement_score` | Agreement score across valid aggregate scores |
| `ensemble_method` | Aggregation method actually used |
| `weights` | Judge weights used by the aggregation method |
| `individual_judge_results` | Valid judge aggregate results with `aggregate_explanation` removed |

## How Scoring Works

1. **Collect judge results** from multiple LLM judges.
2. **Apply ensemble method:**
   - **Majority Vote** (default): Uses mode of scores.
   - **Median**: Uses weighted median of scores.
   - **Average**: Uses weighted average of scores.
3. **Calculate agreement score** to measure consensus among judges:
   - For **categorical** ensemble: the percentage of judges with the same categorical rating.
   - For **numerical** ensemble: `max(0.0, 1.0 - coefficient_of_variation)` (lower variation = higher agreement).
4. **Score distribution** shows how many judges assigned each score value.

## Available Make Commands

```bash
make install             # Install dependencies using uv
make run-homogeneous     # Run homogeneous judge example
make run-heterogeneous   # Run heterogeneous judge example
make clean               # Clean up generated files
```
