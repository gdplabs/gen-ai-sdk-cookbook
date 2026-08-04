# Evaluate Suites from YAML

This example covers the two YAML evaluation flows:

| Flow | Entry point | Demonstrates |
|---|---|---|
| Standard YAML | `evaluate_suites_from_yaml.py` | One YAML file with `ExactMatchMetric` via `class_path`, `KeywordMatchMetric` via registry, model credentials, and a fallback model |
| YAML directory | `evaluate_suites_from_yaml_dir.py` | All SDK sample suites loaded together, including `CompositeEvaluator` |

The standard flow reads only `sample_suites/custom_judge_model_and_metrics_suite.yaml`. The directory flow reads every YAML file under `sample_suites/`.

## Prerequisites

- Python 3.11 or higher
- `uv`
- API keys for the LLM-based suites

## Installation

```bash
uv sync
cp .env.example .env
```

Set `GOOGLE_API_KEY` and `OPENAI_API_KEY` in `.env` before running either example.

## Usage

```bash
make run-standard
make run-directory
```

The directory example includes both deterministic and LLM-based suites, so it uses the configured API keys.
