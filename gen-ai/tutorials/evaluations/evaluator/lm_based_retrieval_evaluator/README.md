# LMBasedRetrievalEvaluator Tutorial

This tutorial demonstrates how to use the **LMBasedRetrievalEvaluator** in the GenAI Evaluator SDK.

The `LMBasedRetrievalEvaluator` evaluates the retrieval step of a RAG pipeline with LLM-based metrics. By default, it runs two metrics:
- **Contextual Precision** — checks whether relevant context is ranked above irrelevant context
- **Contextual Recall** — measures how well the retrieved context aligns with the expected answer

Then it applies a rule engine to classify the retrieval quality (good / bad).

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

The `LMBasedRetrievalEvaluator` accepts `LLMTestCase` objects with the following fields:

- `input` (str) — The user question.
- `expected_output` (str) — The reference or ground truth answer.
- `retrieved_context` (str | list[str]) — The supporting context/documents used during retrieval. Strings are coerced into a single-element list.

Example `LLMTestCase`:

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris is the capital of France.",
    retrieved_context=[
        "Berlin is the capital of Germany.",
        "Paris is the capital city of France with a population of over 2 million people.",
        "London is the capital of the United Kingdom.",
    ],
)
```

## Usage

Run the LM-based retrieval evaluation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the LM-based retrieval evaluation script
make clean      # Clean up generated files
```
