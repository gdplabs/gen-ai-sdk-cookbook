# MetricsAggregator Tutorial

This tutorial demonstrates how to use the **MetricsAggregator** in the GenAI Evaluator SDK.

The `MetricsAggregator` computes `aggregate_success` (AND-gate: all metrics must pass) and `aggregate_score` (polarity-aware mean) across multiple metric results. It also generates human-readable `aggregate_explanation` strings. You can use it directly or supply it to a `CompositeEvaluator` for custom aggregation logic.

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

## Usage

Run the metrics aggregator demo:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the metrics aggregator demo script
make clean      # Clean up generated files
```
