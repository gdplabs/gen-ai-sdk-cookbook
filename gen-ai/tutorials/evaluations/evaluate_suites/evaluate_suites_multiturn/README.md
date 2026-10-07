# Evaluate Suites — Multi-turn

This example runs five conversational suites in one `evaluate_suites` call:

| Suite | Built from | Rows |
|---|---|---|
| `inline` | `ConversationalTestCase` objects in Python | 1 |
| `from_messages` | a chat history of `Message` objects | 1 |
| `from_jsonl` | `sample_data/multiturn_conversations.jsonl`, one conversation per line | 3 |
| `from_csv` | `sample_data/multiturn_conversations.csv`, turns as a JSON string in one column | 3 |
| `multiturn-inline-suite` | `EvalSuite.from_yaml(...)` | 1 |

All five share one `run_id` and one experiment tracker. The script then prints the error raised when a single suite mixes single-turn and multi-turn rows.

## Prerequisites

- Python 3.11 or higher
- `uv`
- A Vertex AI service account for the default judge

## Installation

```bash
make install
cp .env.example .env
```

These examples pass no explicit `models=`, so they use the SDK default judge routed through Vertex. Set these in `.env`:

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

```
{
  "run_id": "default_dataset_20261001T151449Z_70193a80",
  "num_samples": 9
}
inline: 1 row(s)
from_messages: 1 row(s)
from_jsonl: 3 row(s)
from_csv: 3 row(s)
multiturn-inline-suite: 1 row(s)

mixed row types refused: 1 validation error for EvalSuite
data
  Value error, EvalSuite.data mixes row types (ConversationalTestCase, LLMTestCase);
  put single-turn and multi-turn rows in separate suites.
```

The YAML suite takes its name from the file's own `name:` key, and its top-level `test_case_type: ConversationalTestCase` makes the loader validate each row as a conversation. Scores come from an LLM judge and vary between runs.

## Reference

- [Multi-turn Evaluation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/multiturn-evaluation) — conversational suites, turn aggregation, loading options
- `../../metrics/conversational/` — each conversational metric on its own
- `../../evaluator/composite_evaluator_multiturn/` — composing several conversational metrics
