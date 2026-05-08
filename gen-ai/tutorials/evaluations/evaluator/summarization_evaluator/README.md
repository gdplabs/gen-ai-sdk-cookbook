# SummarizationEvaluator Tutorial

This tutorial demonstrates how to use the **SummarizationEvaluator** in the GenAI Evaluator SDK.

The `SummarizationEvaluator` evaluates the quality of a generated summary against its source text (e.g., meeting transcripts).

By default, it runs four metrics:
- **Coherence** — whether the summary is logically organized and flows smoothly
- **Consistency** — factual alignment between summary claims and the source transcript
- **Relevance** — how completely and focused the summary captures important information
- **Fluency** — readability, naturalness, grammar, and clarity of the summary text

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

The `SummarizationEvaluator` accepts `LLMTestCase` objects with the following fields:

- `input` (str) — The source text to be summarized (e.g., a meeting transcript).
- `actual_output` (str) — The generated summary to be evaluated.

Example `LLMTestCase`:

```python
from gllm_evals import LLMTestCase

data = LLMTestCase(
    input="Meeting transcript or source text here...",
    actual_output="Generated summary here...",
)
```

## Usage

Run the summarization evaluation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the summarization evaluation script
make clean      # Clean up generated files
```
