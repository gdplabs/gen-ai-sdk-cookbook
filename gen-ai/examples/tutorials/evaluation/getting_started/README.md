# Getting Started with GenAI Evaluator SDK

This tutorial guides you step-by-step on how to install the GenAI Evaluator SDK and run your first evaluation.

## Prerequisites

Before installing, make sure you have:
- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key (or OpenAI API Key)

## Installation

### 1. Authenticate with Google Cloud

The `gllm-evals` package is hosted in a secure Google Cloud Artifact Registry. You need to authenticate via `gcloud CLI` to access the package.

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

Set your API key as an environment variable:

```bash
# Linux/macOS
export GOOGLE_API_KEY="your_api_key_here"

# Windows PowerShell
$env:GOOGLE_API_KEY = "your_api_key_here"

# Windows Command Prompt
set GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run the evaluation script:

```bash
python eval.py
```

## Understanding the Output

The evaluator will return a JSON response with the following structure:

```json
{
  "generation": {
    "global_explanation": "Summary of evaluation results",
    "relevancy_rating": "bad|good",
    "score": 0.0,
    "possible_issues": ["Retrieval Issue", "Generation Issue"],
    "binary_score": 0,
    "avg_score": 0.6,
    "completeness": {
      "score": 1,
      "explanation": "Detailed explanation...",
      "normalized_score": 0.0
    },
    "groundedness": { ... },
    "redundancy": { ... },
    "language_consistency": { ... },
    "refusal_alignment": { ... }
  }
}
```

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **Completeness** | Measures if the output covers all required information from the expected response |
| **Groundedness** | Checks if the output is supported by the retrieved context |
| **Redundancy** | Identifies unnecessary repetition in the output |
| **Language Consistency** | Ensures the output language matches the input language |
| **Refusal Alignment** | Validates if refusal behavior matches expectations |

## Next Steps

- [Evaluate Helper Function](../evaluate_helper_function/) - Use the convenience `evaluate()` function
- [Custom Evaluators](../create_custom_evaluator_scorer/) - Create your own evaluators and metrics
- [Multiple LLM-as-a-Judge](../multiple_llm_as_a_judge/) - Use multiple judges for better alignment

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluation script
make clean      # Clean up generated files
```
