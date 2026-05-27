# Multi-Domain Customer Service Chatbot — Evaluate Suites Tutorial

This tutorial demonstrates how to evaluate a **multi-domain chatbot** using `evaluate_suites()`. The chatbot handles three customer service domains, each assessed with a different evaluation strategy — all in a single experiment.

## Scenario

A customer service chatbot serves three types of queries:

| Domain | Example Query | Evaluation Strategy |
|---|---|---|
| **FAQ** | "What are your business hours?" | `GEvalGenerationEvaluator` — completeness + redundancy |
| **Knowledge Base RAG** | "How do I reset my password?" | `CompositeEvaluator(groundedness)` — factuality against retrieved context |
| **Troubleshooting** | "The app crashes when uploading photos" | `GEvalGenerationEvaluator` — completeness + redundancy for multi-step guidance |

All three suites are evaluated via a single `evaluate_suites()` call, sharing:
- One **`run_id`** — a single experiment
- One **`CSVExperimentTracker`** — one leaderboard entry
- Per-suite **namespaced dataset names** (`customer_service/faq`, `customer_service/rag`, etc.)

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- OpenAI API Key

## Installation

### 1. Clone the repository & open the directory

```bash
git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/tutorials/evaluate_suites_tutorial
```

### 2. Install dependencies

```bash
make install
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Usage

### Run the default evaluation

```bash
make run
```

This evaluates all three suites with default thresholds. The output includes:
- Per-suite results (`result.suites["faq"]`, `result.suites["rag"]`, etc.)
- Pooled results across all suites (`result.run_aggregators_result`)

### Run the calibrated evaluation

After reviewing initial results with domain experts, we adjust thresholds:

```bash
make run-calibrated
```

**Calibration changes:**
- **Troubleshooting**: `completeness` threshold lowered to `0.5` (partial multi-step advice is acceptable). `redundancy` threshold set to `0.0` (verbose troubleshooting is fine — users need detail).
- **FAQ & RAG**: Strict default thresholds maintained (1.0).

## Key Takeaways

1. **One experiment, different evaluators.** Each suite uses the evaluator most relevant to its domain — not a one-size-fits-all evaluation.
2. **Per-suite aggregation + pooled aggregation.** You get domain-specific metrics AND a holistic picture.
3. **Calibration is per-suite.** Different domains have different expectations — thresholds should reflect that.

## Reference

- [Evaluate Suites Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluate-suites)
- [Evaluate Helper Function Documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evaluate-helper-function)

## Available Make Commands

```bash
make install         # Install dependencies using uv
make run             # Run the multi-domain chatbot evaluation
make run-calibrated  # Run the calibrated evaluation with per-suite thresholds
make clean           # Clean up generated files
```
