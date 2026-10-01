# ConvEvaluator Tutorial

This tutorial demonstrates the **ConvEvaluator** in the GenAI Evaluator SDK.

The `ConvEvaluator` runs several conversational metrics over one `ConversationalTestCase` and aggregates their results into a unified report. It is the conversation-level counterpart to `CompositeEvaluator`: the same composition idea, applied to a whole multi-turn conversation instead of a single row.

## When to Use ConvEvaluator

Use `ConvEvaluator` when what you want to measure only exists **across turns**:

- **A task spanning several turns** — did the booking, the refund, the change of flight actually complete
- **Memory** — did the assistant forget something the user said four turns ago
- **Drift** — did a later answer contradict the document that turn retrieved
- **Scope** — did the assistant stay on its allowed topics and decline the rest
- **A criterion of your own** — judged over the conversation rather than one reply

For single-turn rows use `CompositeEvaluator` instead. A suite holds one kind of row or the other, never both.

## How It Works

1. **Accepts conversational metrics** — any metric whose `supports_conversational` is `True`
2. **Checks requirements per row** — a metric is skipped on a conversation missing a field it needs, rather than scored on partial data
3. **Executes metrics** — concurrently by default, or sequentially with `run_parallel=False`
4. **Aggregates scores** — `MetricsAggregator` for polarity-aware binary scoring
5. **Isolates failures** — one metric erroring does not take down the row

## What this example shows

`conv_evaluation.py` scores two booking conversations with the same three metrics, so the contrast is visible rather than a single number in isolation:

| Conversation | What happens |
| --- | --- |
| `SUCCESSFUL` | searches, presents options, books, and recalls the booking correctly |
| `FAILED` | names the wrong flight as cheapest, refuses to book, then forgets the whole topic |

The metrics are `DeepEvalGoalAccuracyMetric`, `DeepEvalKnowledgeRetentionMetric` and `DeepEvalConversationCompletenessMetric`.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
- A Vertex AI service account — see the note on credentials below

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install dependencies

```bash
make install
```

or:

```bash
uv sync
```

### 3. Configure credentials

```bash
cp .env.example .env
```

The examples pass no explicit `models=`, so they use the SDK default judge, which is routed through **Vertex AI with a service account**:

```dotenv
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_LOCATION=global
GOOGLE_VERTEX_LABEL={"billing-owner":"your-team"}
```

`GOOGLE_VERTEX_LABEL` is required so every Vertex call is attributable to a billing owner. An invoker built without this route refuses to invoke rather than falling back to an API key.

## Running

```bash
make run
```

or:

```bash
uv run python conv_evaluation.py
```

## Expected Output

Each conversation prints one evaluator block: the aggregate fields followed by each metric's score and explanation.

```python
# successful
{
  "aggregate_success": true,
  "aggregate_score": 0.9166666666666666,
  "aggregate_explanation": "All metrics met the expected values.",
  "deepeval_goal_accuracy": {"score": 0.75, "success": true, "explanation": "..."},
  "deepeval_knowledge_retention": {"score": 1.0, "success": true, "explanation": "..."},
  "deepeval_conversation_completeness": {"score": 1.0, "success": true, "explanation": "..."}
}
```

For the failing conversation, `aggregate_explanation` names everything that fell short:

```
"aggregate_success": false,
"aggregate_score": 0.16666666666666666,
"aggregate_explanation": "The following metrics failed to meet expectations:
1. Deepeval Conversation Completeness is 0 (should be >= 0.5)
2. Deepeval Goal Accuracy is 0.16666666666666666 (should be >= 0.5)
3. Deepeval Knowledge Retention is 0.3333333333333333 (should be >= 0.5)"
```

Scores come from an LLM judge and move between runs — treat the numbers above as the shape of the output, not exact values.

## Sequential execution

Set `run_parallel=False` when the judge is rate-limited or you want deterministic log ordering:

```python
ConvEvaluator(metrics=[...], run_parallel=False)
```

## Fault isolation

A metric whose judge fails is recorded with `score=None` and `rubric_score=None` — there was no measurement, which is not the same as scoring zero — plus `error` and `error_type`, and a line in `aggregate_explanation`. The errored metric leaves the aggregate's denominator rather than dragging it to zero.

If **every** metric on a row errors, the row is reported as an evaluator-level error, because there is nothing to aggregate.

To make a whole run refuse to look healthy after losing too many measurements:

```python
await evaluate_suites([suite], max_metric_error_rate=0.0)
# RunError: 4 of 8 metric evaluations errored (50.0%), ceiling 0.0%
```

## Related examples

- `../../metrics/conversational/` — each conversational metric on its own, including turn aggregation
- `../composite_evaluator/` — the single-turn counterpart
- `../../evaluate_suites/evaluate_suites_multiturn/` — running conversational suites end to end
