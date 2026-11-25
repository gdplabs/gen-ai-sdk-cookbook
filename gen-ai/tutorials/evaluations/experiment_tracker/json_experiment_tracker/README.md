# JSON Experiment Tracker Tutorial

Use `JSONExperimentTracker.log()` to save each evaluated row under one run ID. Read the saved row count and average score with `get_run_results()`, then read the project leaderboard with `get_experiment_history()`.

For automatic logging across evaluation suites, see the [standard `evaluate_suites` tutorial](../../evaluate_suites/evaluate_suites_standard/README.md).

## Prerequisites

- Python 3.12 or 3.13
- An OpenRouter API key for the evaluation judge

## Installation

### 1. Install dependencies

With `uv` and Make installed, run:

```bash
make install
```

Or install dependencies in an active Python 3.12 or 3.13 environment:

```bash
pip install "gllm-evals-binary>=0.1.45,<0.2.0" "python-dotenv>=1.0.0,<2.0.0"
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Set `OPENROUTER_API_KEY` in `.env` to the key for the evaluation judge.

## Usage

Run the JSON experiment tracker example:

```bash
make run
```

The example saves two rows under `my_experiments/`. Run it again to see both run IDs in the project history.

If you installed with pip, run `python example_json_experiment_tracker.py` in the same environment.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the JSON experiment tracker script
make clean      # Clean up generated files
```
