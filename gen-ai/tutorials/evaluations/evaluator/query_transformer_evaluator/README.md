# QueryTransformerEvaluator Tutorial

This tutorial demonstrates how to use the **QTEvaluator** in the GenAI Evaluator SDK.

The `QTEvaluator` evaluates query transformation tasks, checking how well queries are rewritten, expanded, or paraphrased for downstream use.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key (or OpenAI API Key)

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

Or manually:

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API key
```

## Input & Output Types

The `QTEvaluator` accepts `LLMTestCase` objects with the following fields:

- `input` (str) — The original input query.
- `actual_output` (str) — The model's transformed query output serialized as a stringified `list[str]`.
- `expected_output` (str) — The reference transformed query serialized as a stringified `list[str]`.

Example `LLMTestCase`:

```python
from gllm_evals.types import LLMTestCase

expected_response = ["penanggung jawab pemantauan", "prosedur pelaporan"]
generated_response = ["penanggung jawab pemantauan", "prosedur pelaporan"]

data = LLMTestCase(
    input="Decompose this query: ...",
    expected_output=str(expected_response),
    actual_output=str(generated_response),
)
```

## Usage

Run the query transformer evaluation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the query transformer evaluation script
make clean      # Clean up generated files
```
