# Composite Evaluator Tutorial — Multi-turn

The `CompositeEvaluator` also runs several conversational metrics over one `ConversationalTestCase` and aggregates their results into a unified report, the same way it does for single-turn rows.

`composite_evaluation_multiturn.py` scores two booking conversations with the same three metrics:

| Conversation | What happens |
|---|---|
| `SUCCESSFUL` | searches, presents options, books, and recalls the booking correctly |
| `FAILED` | names the wrong flight as cheapest, refuses to book, then forgets the topic |

The metrics are `DeepEvalGoalAccuracyMetric`, `DeepEvalKnowledgeRetentionMetric` and `DeepEvalConversationCompletenessMetric`.

## Prerequisites

- Python 3.11 or higher
- `uv`
- A Vertex AI service account for the default judge

## Installation

```bash
make install
cp .env.example .env
```

This example passes no explicit `models=`, so it uses the SDK default judge routed through Vertex. Set these in `.env`:

```dotenv
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_LOCATION=global
GOOGLE_VERTEX_LABEL={"billing-owner":"your-team"}
```

## Usage

```bash
make run
```

## Expected Output

Each conversation prints one evaluator block: the aggregate fields followed by each metric's score and explanation.

```python
{
  "aggregate_success": true,
  "aggregate_score": 0.9166666666666666,
  "aggregate_explanation": "All metrics met the expected values.",
  "deepeval_goal_accuracy": {"score": 0.75, "success": true, "explanation": "..."},
  "deepeval_knowledge_retention": {"score": 1.0, "success": true, "explanation": "..."},
  "deepeval_conversation_completeness": {"score": 1.0, "success": true, "explanation": "..."}
}
```

For the failing conversation, `aggregate_explanation` lists every metric that fell short:

```
"aggregate_success": false,
"aggregate_score": 0.16666666666666666,
"aggregate_explanation": "The following metrics failed to meet expectations:
1. Deepeval Conversation Completeness is 0 (should be >= 0.5)
2. Deepeval Goal Accuracy is 0.16666666666666666 (should be >= 0.5)
3. Deepeval Knowledge Retention is 0.3333333333333333 (should be >= 0.5)"
```

Scores come from an LLM judge and vary between runs. An errored metric is recorded with `score=None` plus `error` and `error_type`, and leaves the aggregate's denominator rather than counting as zero.

## Reference

- [Composite Evaluator Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluator/composite-evaluator#evaluating-conversations)
- [Multi-turn Evaluation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/multiturn-evaluation)
- `../../metrics/conversational/` — each conversational metric on its own
- `../composite_evaluator/` — the same evaluator on single-turn rows
