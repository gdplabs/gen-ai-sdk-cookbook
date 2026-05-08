# ClassicalRetrievalEvaluator Tutorial

This tutorial demonstrates how to use the **ClassicalRetrievalEvaluator** in the GenAI Evaluator SDK.

The `ClassicalRetrievalEvaluator` evaluates retrieval performance with classical IR metrics: MAP, NDCG, Precision, Recall, and Top-K Accuracy. It is fast, deterministic, and ideal for benchmarking retrieval systems where interpretability and reproducibility are key.

## Prerequisites

- Python 3.11 or higher

## Installation

Using `uv` (recommended):

```bash
make install
```

Or manually:

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```

## Input & Output Types

The `ClassicalRetrievalEvaluator` accepts `RetrievalData` with `retrieved_chunks` (dict of chunk ID to score) and `ground_truth_chunk_ids` (list of relevant chunk IDs).

Example `RetrievalData`:

```python
from gllm_evals.types import RetrievalData

data = RetrievalData(
    retrieved_chunks={
        "chunk1": 9.0,
        "chunk2": 0.0,
        "chunk3": 0.3,
        "chunk4": 0.1,
        "chunk5": 0.2,
        "chunk6": 0.4,
        "chunk7": 0.5,
        "chunk8": 0.6,
        "chunk9": 0.7,
        "chunk10": 0.8,
    },
    ground_truth_chunk_ids=["chunk9", "chunk3", "chunk2"],
)
```

## Usage

Run the classical retrieval evaluation example:

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the classical retrieval evaluation script
make clean      # Clean up generated files
```
