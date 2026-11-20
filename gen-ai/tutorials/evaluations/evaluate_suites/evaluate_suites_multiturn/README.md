# Evaluate Suites — Multi-turn

This example runs four conversational suites in one `evaluate_suites` call:

| Suite | Built from | Rows |
|---|---|---|
| `inline` | `ConversationalTestCase` objects in Python | 1 |
| `from_messages` | a chat history of `Message` objects | 1 |
| `from_jsonl` | `sample_data/multiturn_conversations.jsonl`, one conversation per line | 3 |
| `from_csv` | `sample_data/multiturn_conversations.csv`, turns as a JSON string in one column | 3 |

Each line is one conversation: `turns` (required), plus optional `test_case_id`, `expected_output`, `chatbot_role` and `scenario`.
Every row in one run needs its own `test_case_id`. A row without one gets an id from its content, so the JSONL and CSV samples, which hold the same three conversations, set different ids.
A turn has `role` (`user` or `assistant`), `content`, and on assistant turns optional `retrieved_context`
(a list of strings) and `tools_called` (`name`, `input_parameters`, `output`).
See [ConversationalTestCase](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/conversationaltestcase) for every field.

All four share one `run_id` and one experiment tracker. The script then prints the error raised when a single suite mixes single-turn and multi-turn rows.

## Prerequisites

- Python 3.12 or higher
- `uv`
- An OpenRouter API key for the default judge

## Installation

```bash
make install
cp .env.example .env
```

These examples pass no explicit `models=`, so they use the SDK default judge through OpenRouter. Set this in `.env`:

```dotenv
# The default judge, openrouter/deepseek/deepseek-v4.1-flash-1017, reads this key
OPENROUTER_API_KEY=sk-or-...
```

## Usage

```bash
make run
```

A judge call can time out (`GLLM-EVAL-TIMEOUT`); rerun the script. If a metric errors, `evaluate_suites` raises after saving the results; pass `raise_on_error=False` to keep a run with errored metrics.

## Expected Output

```
{
  "run_id": "default_dataset_20261116T031750Z_51eb87fa",
  "num_samples": 8
}
inline: 1 row(s)
from_messages: 1 row(s)
from_jsonl: 3 row(s)
from_csv: 3 row(s)

mixed row types refused: 1 validation error for EvalSuite
data
  Value error, EvalSuite.data mixes row types (ConversationalTestCase, LLMTestCase);
  put single-turn and multi-turn rows in separate suites.
```

Scores come from an LLM judge and vary between runs.

## Reference

- [Multi-turn Evaluation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/multiturn-evaluation) — conversational suites, turn aggregation, loading options
- `../../metrics/conversational/` — each conversational metric on its own
- `../../evaluator/composite_evaluator_multiturn/` — composing several conversational metrics
