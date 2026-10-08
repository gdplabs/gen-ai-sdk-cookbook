# Environment State Metric

This tutorial demonstrates how to evaluate captured environment snapshots (such as a mailbox) against expected rules using a custom `EmailSentVerificationMetric`. It verifies if an agent successfully completed its task (like sending the correct emails) based on the actual resulting state of the environment, rather than relying on a subjective LLM judge.

See the full tutorial: [Environment State Metric on Weekly Report Orchestrator Agent](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/environment-state-metric-weekly-report)

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- `gcloud` CLI authenticated (`gcloud auth login`)
- Access to the `gen-ai-internal` package index

## Setup & Running

Because the internal package registry requires authentication, you need to expose your `gcloud` credentials to `uv` as environment variables. 

```bash
export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_INTERNAL_PASSWORD=$(gcloud auth print-access-token)
```

Then, you can simply run the script. `uv` will automatically install the necessary dependencies according to the `pyproject.toml` file and execute the evaluation:

```bash
uv run quickstart.py
```

The script will output a PASS or FAIL score for each case based on whether the mailbox state matches the expected emails.

## Project Structure

```text
environment_state_metric/
├── dataset/
│   └── quickstart_cases.jsonl  # Synthetic labelled cases
├── pyproject.toml              # Dependencies and uv configuration
├── quickstart.py               # Defines custom metric and runs the evaluation
└── uv.lock                     # Lockfile for reproducible dependencies
```

## Dataset

The dataset (`dataset/quickstart_cases.jsonl`) contains synthetic, labelled cases for email verifications. Each row provides:
- `expected_emails`: The checklist of rules the email should contain (e.g., subject, content).
- `actual_emails`: The actual mailbox state that was captured after the agent acted.
- `label`: The expected `PASS`/`FAIL` outcome of the metric.
