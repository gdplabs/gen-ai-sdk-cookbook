# Multiple LLM-as-a-Judge

Multiple LLM-as-a-Judge is an advanced evaluation approach that uses multiple language models as judges to evaluate tasks in parallel and aggregate their results using ensemble methods.

## Benefits

| Benefit | Description |
|---------|-------------|
| **Higher Alignment** | Multiple judges provide more reliable and consistent evaluations |
| **Faster Human Annotation** | Humans only review cases where agreement < 100% |
| **Human Alignment** | 100% agreement score indicates high alignment with human judgment |

## Quick Start

### 1. Install Dependencies

```bash
make install
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the Example

```bash
make run
```

## Usage

### Basic Example

```python
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.judge.multiple_llm_as_judge import MultipleLLMAsJudge
from gllm_evals import load_simple_qa_dataset

# Define multiple judge models
judge_models = [
    {
        "provider_model_id": "openai/gpt-4o",
        "model_credentials": os.getenv("OPENAI_API_KEY"),
    },
    {
        "provider_model_id": "openai/gpt-4.1",
        "model_credentials": os.getenv("OPENAI_API_KEY"),
    },
]

# Create evaluator with multiple judges
evaluator = GEvalGenerationEvaluator(
    judge=MultipleLLMAsJudge(judge_models=judge_models),
    model_credentials=os.getenv("GOOGLE_API_KEY"),
)

# Evaluate
data = load_simple_qa_dataset()
result = await evaluator.evaluate(data.dataset[0])
```

### Custom Weights

Assign different weights to each judge:

```python
judge_models = [
    {
        "provider_model_id": "openai/gpt-4o",
        "model_credentials": os.getenv("OPENAI_API_KEY"),
        "weight": 2.0,  # This judge has 2x influence
    },
    {
        "provider_model_id": "openai/gpt-4.1",
        "model_credentials": os.getenv("OPENAI_API_KEY"),
        "weight": 1.0,  # Default weight
    },
]
```

### Ensemble Methods

Choose how results are aggregated:

```python
# Median (default, recommended)
judge = MultipleLLMAsJudge(
    judge_models=judge_models,
    ensemble_method="median",
)

# Average rounded
judge = MultipleLLMAsJudge(
    judge_models=judge_models,
    ensemble_method="average_rounded",
)
```

## Understanding the Output

```json
{
  "generation": {
    "global_explanation": "...",
    "ensemble_relevancy_rating": "good",
    "ensemble_method": "median",
    "weights": [1, 1],
    "agreement_score": 1.0,
    "judge_variance": 0.0,
    "individual_judge_results": [
      {
        "relevancy_rating": "good",
        "score": 1.0,
        "completeness": {"score": 3, ...},
        "groundedness": {"score": 3, ...},
        "provider_model_id": "openai/gpt-4o",
        ...
      },
      {
        "relevancy_rating": "good",
        "score": 1.0,
        "provider_model_id": "openai/gpt-4.1",
        ...
      }
    ]
  }
}
```

### Output Fields

| Field | Description |
|-------|-------------|
| `ensemble_relevancy_rating` | Aggregated categorical rating (good/bad) |
| `ensemble_method` | Method used for aggregation |
| `weights` | Weights assigned to each judge |
| `agreement_score` | 0.0 to 1.0, higher = more consensus |
| `judge_variance` | Statistical variance among judges |
| `individual_judge_results` | Each judge's detailed evaluation |

### Agreement Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 1.0 | All judges agree | High confidence, no review needed |
| < 1.0 | Some disagreement | Human review recommended |

## Supported Model Providers

The `provider_model_id` uses the format `provider/model_name`:

- OpenAI: `openai/gpt-4o`, `openai/gpt-4.1`, `openai/gpt-3.5-turbo`
- Google: `google/gemini-pro`, `google/gemini-3-pro`
- Anthropic: `anthropic/claude-3-opus`, `anthropic/claude-3-sonnet`

## Production Tips

1. **Choose diverse models**: Use models from different providers for better coverage
2. **Adjust weights**: Give more weight to more reliable judges
3. **Monitor agreement scores**: Low agreement indicates need for human review
4. **Use appropriate ensemble method**: Median is more robust to outliers

## Available Make Commands

```bash
make install    # Install dependencies using Poetry
make run        # Run the evaluation examples
make clean      # Clean up generated files
```

## Next Steps

- [Custom Evaluators](../create_custom_evaluator_scorer/) - Create your own evaluators
- [Evaluate Helper Function](../evaluate_helper_function/) - Use the convenience function
