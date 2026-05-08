# Modify Metrics Tutorial

This tutorial demonstrates how to **modify existing metric attributes** in the GenAI Evaluations SDK.

## Example: Recalibrating Context Sufficiency for RAG Pipelines

The default `GEvalContextSufficiencyMetric` checks whether context contains enough information to answer a query. A RAG-heavy evaluation might need different threshold boundaries, domain-specific few-shot examples, and refined rubric wording.

### What Changed From the Default

| Attribute | Default | Modified |
|-----------|---------|----------|
| `rubric` | Standard scoring | Refined scoring boundaries for calculation-heavy evaluation |
| `additional_context` | None | Added few-shot examples that distinguish "calculable from data" vs "requires assumption" |
| `threshold` | `0.5` | `0.75` — stricter context sufficiency checks |

The metric class itself is unchanged. No subclassing needed.

### Common Attributes to Override

| Attribute | Description |
|-----------|-------------|
| `criteria` | Main instruction for what the judge evaluates |
| `evaluation_steps` | Ordered reasoning steps the judge follows |
| `additional_context` | Extra prompt context, often few-shot examples |
| `rubric` | Score ranges and expected outcomes |
| `threshold` | Pass/fail cutoff |
| `strict_mode` | Force stricter binary-style pass/fail behavior when supported |

If modifying these attributes still cannot express your evaluation need, create a custom metric instead. See the [Custom Metric](../custom_metric) tutorial.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key

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

Run the modify metrics example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the modify context sufficiency script
make clean      # Clean up generated files
```
