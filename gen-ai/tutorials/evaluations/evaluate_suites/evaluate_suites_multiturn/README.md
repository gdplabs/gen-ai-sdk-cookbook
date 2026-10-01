# Evaluate Suites — Multi-turn

This example runs **multi-turn conversations** through `evaluate_suites`, covering every way a conversational suite is built and the one rule that trips people up.

| Suite | Built from | Rows |
| --- | --- | --- |
| `inline` | `ConversationalTestCase` objects in Python | 1 |
| `from_messages` | a chat history of `Message` objects | 1 |
| `from_csv` | a CSV whose `turns` column holds a JSON array | 3 |
| `multiturn-inline-suite` | `EvalSuite.from_yaml(...)` | 1 |

All four run in one `evaluate_suites` call, sharing one `run_id` and one experiment tracker.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (`gcloud` CLI) installed
- A Vertex AI service account

## Installation

```bash
gcloud auth login
make install      # or: uv sync
cp .env.example .env
```

This example passes no explicit `models=`, so it uses the SDK default judge, routed through **Vertex AI with a service account**:

```dotenv
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_LOCATION=global
GOOGLE_VERTEX_LABEL={"billing-owner":"your-team"}
```

`GOOGLE_VERTEX_LABEL` is required so each Vertex call is attributable to a billing owner. An invoker built without this route refuses to invoke rather than falling back to an API key.

## Running

```bash
make run          # or: uv run python evaluate_suites_multiturn.py
```

## Expected Output

```
{
  "run_id": "default_dataset_20261001T151449Z_70193a80",
  "num_samples": 6
}
inline: 1 row(s)
from_messages: 1 row(s)
from_csv: 3 row(s)
multiturn-inline-suite: 1 row(s)

mixed row types refused: 1 validation error for EvalSuite
data
  Value error, EvalSuite.data mixes row types (ConversationalTestCase, LLMTestCase);
  put single-turn and multi-turn rows in separate suites.
```

Note the YAML suite takes its name from the file's own `name:` key, not from the Python call.

## The four ways to build a conversational suite

### Inline

`retrieved_context` and `tools_called` belong to the **turn**, not the conversation — that is what lets a metric judge each assistant answer against the context that answer actually had.

```python
ConversationalTestCase(
    turns=[
        Turn(role="user", content="Book me a flight to Paris next Friday."),
        Turn(
            role="assistant",
            content="I found two options: Air France $320 and Delta $410.",
            retrieved_context=["Air France CDG 09:15 $320", "Delta CDG 14:40 $410"],
            tools_called=[ToolCall(name="search_flights", output="Air France $320; Delta $410")],
        ),
    ],
    chatbot_role="a helpful travel booking assistant",
    expected_output="The assistant searches, presents options, and completes the booking.",
)
```

### From a chat history

The system message becomes `chatbot_role`:

```python
ConversationalTestCase.from_messages(
    [
        Message.system("You are a cautious health information assistant."),
        Message.user("What are the side effects of ibuprofen?"),
        Message.assistant("Common side effects include stomach upset, nausea, and headache."),
    ]
)
```

### From a CSV

`sample_data/multiturn_conversations.csv` stores the turns as a JSON array in one column. Name that column in `json_columns` so it is parsed rather than read as a string:

```python
DictDataset.from_csv(
    "sample_data/multiturn_conversations.csv",
    test_case_type=ConversationalTestCase,
    json_columns=["turns"],
).load()
```

Other columns map to conversation-level fields — `expected_output`, `chatbot_role`, `scenario`.

### From YAML

`sample_suites/multiturn_inline_suite.yaml` declares its rows, evaluator and metrics, so `EvalSuite.from_yaml` needs nothing else:

```python
EvalSuite.from_yaml("sample_suites/multiturn_inline_suite.yaml")
```

The key that makes it conversational is at the top level:

```yaml
test_case_type: ConversationalTestCase
```

In a `dataset:` suite, that same key lives under `dataset.kwargs` instead.

## A suite cannot mix row types

One `EvalSuite` holds either single-turn rows or conversations. Mixing them is rejected when the suite is constructed — before any judge is called — rather than part-way through a run. `show_mixed_rows_are_rejected()` in the script demonstrates it.

The exception is a pydantic `ValidationError`, which is itself a `ValueError`, so `except ValueError` catches it.

Put the two kinds in separate suites and pass both to `evaluate_suites`.

## Refusing a run that lost too many measurements

A metric whose judge fails is recorded with `score=None` plus `error` and `error_type`, rather than counting as zero. That keeps the number honest, but a nightly run can still finish green after losing a large share of its measurements. Set a ceiling to turn that into a failure:

```python
await evaluate_suites(suites, max_metric_error_rate=0.0)
# RunError: 4 of 8 metric evaluations errored (50.0%), ceiling 0.0%
```

`RunError` is importable from `gllm_evals`. The ceiling is validated when the call starts, so an out-of-range value fails before any judge is paid for. Leaving it unset keeps the previous behaviour.

## Related examples

- `../../metrics/conversational/` — each conversational metric on its own, plus turn aggregation
- `../../evaluator/conv_evaluator/` — composing several conversational metrics
- `../evaluate_suites_from_yaml/` — the YAML format in depth, single-turn
