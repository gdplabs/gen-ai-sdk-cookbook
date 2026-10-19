# Environment State Metric

This tutorial demonstrates how to evaluate captured environment snapshots (such as mailbox, Google Docs, and Google Sheets) against expected rules using modular, production-aligned verification metrics (`EmailSentVerificationMetric`, `DocsContentVerificationMetric`, `SheetRecipientVerificationMetric`). It verifies if an agent successfully completed its task based on the actual resulting state of the environment, rather than relying on a subjective LLM judge.

See the full tutorial: [Environment State Metric on Weekly Report Orchestrator Agent](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/environment-state-metric-weekly-report)

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- `gcloud` CLI authenticated (`gcloud auth login`)
- Access to the `gen-ai-internal` package index

## Setup & Running

Because the internal package registry requires authentication, you need to expose your `gcloud` credentials to `uv` as environment variables:

```bash
export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_INTERNAL_PASSWORD=$(gcloud auth print-access-token)
```

Then, you can run the evaluation tutorial using `uv`:

```bash
uv run tutorial.py
```

The script groups cases by `suite_name` (`saturday-create`, `saturday-remind`, `saturday-share`), wires each suite to its corresponding evaluator with verification metrics, and evaluates them in a single `evaluate_suites` execution to compute the True Positive Rate (TPR) and True Negative Rate (TNR).

## Project Structure

```text
environment_state_metric/
├── dataset/
│   └── calibration.jsonl           # Model/agent runs and environment state snapshots
├── metrics/                        # Modular verification metric package
│   ├── __init__.py                 # Exports verification metrics
│   ├── _content_matching.py        # Literal and regex content matching
│   ├── _doc_links.py               # Google Docs link extraction
│   ├── _email_query.py             # Email pool search and filtering
│   ├── _row_fields.py              # LLMTestCase attribute accessors
│   ├── _subject_matching.py        # Whole-word subject matching
│   ├── docs_content_verification.py    # DocsContentVerificationMetric implementation
│   ├── email_sent_verification.py     # EmailSentVerificationMetric implementation
│   └── sheet_recipient_verification.py # SheetRecipientVerificationMetric implementation
├── pyproject.toml                  # Dependencies and uv configuration
├── tutorial.py                     # Suite calibration runner with run_aggregators
└── uv.lock                         # Lockfile for reproducible dependencies
```

## Dataset

The dataset (`dataset/calibration.jsonl`) contains labelled test cases derived from environment oracle runs. Each row provides:
- `expected_emails`: The checklist of expected rules (subject contains/excludes, content, required recipients).
- `actual_emails`: The observed mailbox state captured after agent execution.
- `excluded_recipients`: Addresses that must never receive an email.
- `label`: The ground-truth outcome (`PASS` or `FAIL`) used to calibrate the metric.
