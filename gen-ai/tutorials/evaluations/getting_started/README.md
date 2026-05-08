# Getting Started with GenAI Evaluator SDK

This tutorial will guide you step-by-step on how to install the GenAI Evaluator SDK and run your first evaluation.

## Prerequisites

Before installing, make sure you have:
- [Python 3.11+](https://glair.gitbook.io/hello-world/prerequisites)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) - required because `gllm-evals` is a private library hosted in a private Google Cloud repository

## Installation

### 1. Authenticate with Google Cloud

The `gllm-evals` package is hosted in a secure Google Cloud Artifact Registry. You need to authenticate via `gcloud CLI` to access and download the package during installation.

```bash
gcloud auth login
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
# Install the gllm-evals package with optional dependencies
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

### 3. Set Up Environment Variables

Copy the example environment file and add your API key:

```bash
cp .env.example .env
# Edit .env with your API key
```

Set a valid language model credential as an environment variable. This API Key will be used for evaluators that uses LLM as judge.

In this example, let's use an Google API Key.
Get an Google API key from [Google AI Studio](https://aistudio.google.com/api-keys).

```bash
# Linux/macOS
export GOOGLE_API_KEY="your_api_key_here"

# Windows PowerShell
$env:GOOGLE_API_KEY = "your_api_key_here"

# Windows Command Prompt
set GOOGLE_API_KEY=your_api_key_here
```

## LLMTestCase

LLMTestCase is the canonical input type for all evaluators. It holds your precomputed model outputs and any supporting context needed for evaluation.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | `str` | ✓ | The user question or prompt. |
| `actual_output` | `str` | ✓ | The model's generated response to evaluate. |
| `expected_output` | `str` | optional | The reference or ground truth answer. |
| `retrieved_context` | `str \| list[str]` | optional | Supporting context/documents used during generation (e.g., RAG retrieved chunks). |
| `tools_called` | `list[dict]` | optional | Actual tools called by the agent. |
| `expected_tools` | `list[dict]` | optional | Reference tools expected to be called. |
| `agent_trajectory` | `list[dict]` | optional | Full agent trajectory (parsed as tools_called if tools_called is not provided). |
| `expected_agent_trajectory` | `list[dict]` | optional | Reference trajectory for comparison. |

`actual_output` must be provided by you — the evaluators do not run inference. You are responsible for generating model responses beforehand and populating this field before calling `evaluate()`.

Not every evaluator uses every field — each evaluator only reads the fields it needs and skips metrics that are missing required data.

## Running Your First Evaluation

In this tutorial, we will evaluate RAG pipeline output.
Create a script called `eval.py`. Choose one of the following approaches based on your needs:

### Approach 1: Simple Metric Evaluation

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import GEvalCompletenessMetric


async def main() -> None:
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="New York",
        expected_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

### Approach 2: Full Generation Evaluator with Custom Model

```python
import asyncio
import os

from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase


async def main():
    model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    evaluator = GEvalGenerationEvaluator(models=model)
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

Run the script:

```bash
python eval.py
```

By default, eval uses Gemini 3 Flash from Google as its model. If you want to use your own model, pass a BaseLMInvoker via the `models` parameter, or pass `models=[invoker] * N` for multi-judge evaluation.

## Understanding the Output

The evaluator will return a JSON response with the following structure:

```json
{
  "generation": {
    "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Completeness is 0 (should be 0.5)\n2. Groundedness is 0 (should be 0.5)",
    "aggregate_success": false,
    "aggregate_score": 0.3333333333333333,
    "completeness": {
      "score": 0.0,
      "explanation": "The minimum key facts are: [Paris]. The Generated Response identifies 'New York' as the capital, which directly contradicts the expected fact [Paris] per Step 5A. Since the single required key fact is contradicted and not matched, the response fails to provide a correct answer per Step 5C Coverage Rule.",
      "rubric_score": 1,
      "success": false,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "redundancy": {
      "score": 0.0,
      "explanation": "The response consists of a single phrase with no repeated words or paraphrased ideas. Each element of the answer is presented only once, maintaining high conciseness without any redundancy.",
      "rubric_score": 1,
      "success": true,
      "threshold": 0.4,
      "strict_mode": false,
      "higher_is_better": false
    },
    "groundedness": {
      "score": 0.0,
      "explanation": "The output provides 'New York' as the answer, which is a critical factual contradiction of the retrieval context stating that 'Paris is the capital of France.'",
      "rubric_score": 1,
      "success": false,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "is_refusal": false
  }
}
```

Congratulations! You have successfully run your first evaluation.

## Recommendation

If you want to run an end-to-end evaluation, use the [evaluate() helper function](../evaluate_helper_function/) instead of the step-by-step commands above.
It will automatically handle experiment tracking (via the Experiment Tracker) and integrates results into your existing [Dataset](../dataset/), so you don't have to wire these pieces together manually.

## Next Steps

You're now ready to start using our evaluators. We offer several prebuilt evaluators to get you started:

1. [GEvalGenerationEvaluator](../evaluator/)
2. [AgentEvaluator](../evaluator/)
3. [QueryTransformerEvaluator](../evaluator/)
4. [ClassicalRetrievalEvaluator](../evaluator/)

Looking for something else? [Build your own custom evaluator here.](../create_custom_evaluator_scorer/)

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluation script
make clean      # Clean up generated files
```
