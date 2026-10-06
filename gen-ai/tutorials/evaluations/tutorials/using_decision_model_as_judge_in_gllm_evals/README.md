# Using Decision Model as Judge in gllm-evals

This tutorial judges a GEval metric with a decision model, reads the confidence behind its decision, and escalates the case to a stronger language model when that confidence is missing or below a confidence threshold.

A decision model evaluates a choice-type question by selecting a label from the metric's rubric. It returns the chosen label, confidence in that choice, and probabilities for the available choices. The confidence is separate from the output's quality score and its pass/fail `threshold`.

> [!NOTE]
> **Decision models are currently supported only on GEval.** This includes built-in GEval metrics and custom metrics extending `DeepEvalGEvalMetric`. Pass a decision model invoker through `models`. To use Jev (`openrouter/typesafe/jev-1.13`), explicitly select it with `build_dm_invoker()` and set `OPENROUTER_API_KEY`.

See the full tutorial: [Using Decision Model as Judge in gllm-evals](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/using-decision-model-as-judge-in-gllm-evals)

To choose between a decision model and an LLM as judge, see [Decision Model vs LLM](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/using-decision-model-as-judge-in-gllm-evals#decision-model-vs-llm).

## How It Works

| Script | GitBook section | Description |
|--------|-----------------|-------------|
| `read_judge_decision.py` | Quickstart: Read a Judge's Decision | Judges answer completeness with Jev (`openrouter/typesafe/jev-1.13`) and prints the full result, including `decision` |
| `escalate_to_stronger_model.py` | Escalate to a Stronger Model | Judges the case with Jev first, then re-judges it with a stronger language model when confidence is missing or below `CONFIDENCE_THRESHOLD` (`0.8`) |

The scripts are identical to the GitBook code. For what each result field means, see [Understand the Confidence](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/using-decision-model-as-judge-in-gllm-evals#understand-the-confidence).

## Expected Output

### `make run-quickstart`

```python
{
    "score": 0.5,
    "explanation": 'Completeness scored 2 with confidence 0.78. Probabilities: {"1": 0.07, "2": 0.78, "3": 0.15}',
    "rubric_score": 2,
    "success": False,
    "threshold": 1.0,
    "strict_mode": False,
    "higher_is_better": True,
    "token_usage": {
        "openrouter/typesafe/jev-1.13": {
            "input_tokens": 3489,
            "output_tokens": 38,
            "input_token_details": None,
            "output_token_details": None,
        },
    },
    "decision": {
        "model_id": "openrouter/typesafe/jev-1.13",
        "choice": "2",
        "confidence": 0.78,
        "probabilities": {"1": 0.07, "2": 0.78, "3": 0.15},
    },
    "model_id": "openrouter/typesafe/jev-1.13",
}
```

### `make run-escalation`

When the initial confidence is below `0.8`:

```text
Initial confidence: 0.78
Escalated: True
Final score: 0.5
Final judge: openai/gpt-6-luna
```

These values are illustrative; model judgments, confidence, and token usage can vary. The escalated result comes from a language model, so it has `decision=None`.

## Calibrate the Confidence Threshold

The `0.8` confidence threshold is an example. Choose yours against SME-labeled cases as described in [Calibrate the Confidence Threshold](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/using-decision-model-as-judge-in-gllm-evals#calibrate-the-confidence-threshold); the [Calibrating Evals](../calibrating_evals/) tutorial shows the calibration loop.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- An OpenRouter API Key (for Jev)
- An OpenAI API Key (for the stronger model in the escalation example)
- Text-only `LLMTestCase` rows with precomputed `actual_output` and reference `expected_output` values (both scripts include one)

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
make install
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

```bash
make run
```

The scripts read `OPENROUTER_API_KEY` and `OPENAI_API_KEY` from the environment. Without `make`, load `.env` through `uv`:

```bash
uv run --env-file .env python read_judge_decision.py
uv run --env-file .env python escalate_to_stronger_model.py
```

## Available Make Commands

```bash
make help            # List all commands
make install         # Install dependencies
make run             # Run both examples
make run-quickstart  # Read a decision model judge's decision
make run-escalation  # Escalate a low-confidence result to a stronger model
make clean           # Clean up generated files
```
