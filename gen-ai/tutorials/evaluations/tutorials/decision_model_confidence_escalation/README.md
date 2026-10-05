# Tutorial Escalating Low Confidence Result by Decision Model

This tutorial judges a GEval metric with a decision model, reads the confidence behind its decision, and escalates the case to a stronger language model when that confidence is missing or below a confidence cutoff.

A decision model selects a label from the metric's rubric and returns the chosen label, its confidence in that choice, and the probabilities of every label. The confidence is separate from the output's quality score: a confident judgment can still fail, and an unconfident one can still pass.

See the full tutorial: [Tutorial Escalating Low Confidence Result by Decision Model](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/decision-model-confidence-escalation)

## How It Works

| Script | GitBook section | Description |
|--------|-----------------|-------------|
| `read_judge_decision.py` | Quickstart: Read a Judge's Decision | Judges answer completeness with Jev (`openrouter/typesafe/jev-1.13`) and prints the full result, including `decision` |
| `escalate_to_stronger_model.py` | Escalate to a Stronger Model | Judges the case with Jev first, then re-judges it with a stronger language model when confidence is missing or below `CONFIDENCE_THRESHOLD` (`0.8`) |

For what each result field means, see [Understand the Confidence](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/decision-model-confidence-escalation#understand-the-confidence).

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
    "token_usage": None,
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

## Calibrate the Confidence Cutoff

The `0.8` cutoff is an example. Choose yours against SME-labeled cases as described in [Calibrate the Confidence Cutoff](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/decision-model-confidence-escalation#calibrate-the-confidence-cutoff); the [Calibrating Evals](../calibrating_evals/) tutorial shows the calibration loop.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- An OpenRouter API Key (for Jev)
- An OpenAI API Key (for the stronger model in the escalation example)

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

## Available Make Commands

```bash
make help            # List all commands
make install         # Install dependencies
make run             # Run both examples
make run-quickstart  # Read a decision model judge's decision
make run-escalation  # Escalate a low-confidence result to a stronger model
make clean           # Clean up generated files
```
