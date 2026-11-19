# Banking Assistant Chatbot evaluations

`tests/evals/eval_banking_assistant_chatbot.py` runs the chatbot (`chatbot/banking_assistant_chatbot.py`) once on each case in `data/data.jsonl` and
scores the answers with gllm-evals. It is a benchmark: every score is recorded, there is no pass/fail gate.

> **Warning:** each run makes up to 3 paid OpenRouter calls per case to the chatbot (guardrail, relevance, generation,
> DeepSeek V4.1 Flash) plus the Jev judge calls.

## Prerequisites

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | The chatbot's model calls and the Jev 1.14 judge |

Python packages: `gllm-evals-binary`, `python-dotenv` (see `pyproject.toml`).

## Run

```bash
python tests/evals/eval_banking_assistant_chatbot.py   # from the tutorial root
```

Scores go to `tests/evals/results/` (`leaderboard.json` and `experiment_results/`).

## Cases and metrics

`banking_assistant_chatbot_assignment.py` assigns each case to a suite; `evaluators.py` defines the metrics; `metric-assignment.md` says why.

| Suite | Cases | Metrics |
|-------|-------|---------|
| `answerable` | 1, 4, 5, 6, 7, 26, 31 | GEvalCompleteness (1.0), GEvalGroundedness (1.0), GEvalLanguageConsistency (0.5) |
| `refusal` | 54, 58, 70 | GEvalRefusalAlignment (0.5) |

## Results

Each suite's aggregate is printed. A case passes when every metric of its suite passes. A case where the chatbot raised
is listed as "not scored" and the script exits non-zero. A metric's evaluation error is recorded as an error, never as a judge fail.
