# GEvalGenerationEvaluator Tutorial

This tutorial demonstrates how to use the **GEvalGenerationEvaluator** in the GenAI Evaluator SDK.

The `GEvalGenerationEvaluator` evaluates the response/answer of a QnA system, including general chatbots, RAG systems, or agents that answer specific questions.

By default, it runs three metrics:
- **Completeness** — how completely the answer addresses the question
- **Groundedness** — whether claims are supported by retrieved context
- **Redundancy** — whether the answer contains repetitive information

You can additionally enable language consistency and refusal alignment through evaluator configuration.

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

The `GEvalGenerationEvaluator` accepts `LLMTestCase` objects with the following fields:

- `input` (str) — The user question.
- `actual_output` (str) — The model's output to be evaluated.
- `expected_output` (str, optional) — The reference or ground truth answer.
- `retrieved_context` (str, optional) — The supporting context used during generation.

Example `LLMTestCase`:

```python
from gllm_evals import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris",
    actual_output="New York",
    retrieved_context="Paris is the capital of France.",
)
```

## Single vs Batch Evaluation

### Single Evaluation

Evaluate a single test case:

```python
evaluator = GEvalGenerationEvaluator()
result = await evaluator.evaluate(data)
```

### Batch Evaluation

Evaluate multiple test cases at once:

```python
evaluator = GEvalGenerationEvaluator()
results = await evaluator.evaluate([data1, data2, data3])
```

## Usage

Run the single evaluation example:

```bash
make run
```

Run the batch evaluation example:

```bash
make run-batch
```

## Available Make Commands

```bash
make install       # Install dependencies using uv
make run           # Run the single evaluation script
make run-batch     # Run the batch evaluation script
make clean         # Clean up generated files
```
