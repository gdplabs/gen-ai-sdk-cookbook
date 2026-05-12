# Agent QnA Evaluations

This example demonstrates how to evaluate an AI agent pipeline using the GL SDK evaluation module. It includes two scripts:

- **`eval.py`** — multi-case CSV-based evaluation using mock tool call outputs
- **`eval_calibrated.py`** — calibrated evaluation that replaces `completeness` with `DeepEvalToolCorrectnessMetric` + `GEvalContextSufficiencyMetric` for multi-item queries

## 🚀 Getting Started

1. **Set UV authentication and install dependencies**
   
   Run the following command to sync dependencies:
   ```bash
   make sync
   ```

2. **Prepare `.env` file**
   
   Create a `.env` file based on `.env.example` and set your `GOOGLE_API_KEY`.
   ```bash
   cp .env.example .env
   ```

3. **Run the CSV-based multi-case evaluation**
   
   ```bash
   make run-eval
   ```

   The script loads `data/eval_dataset.csv` (3 test cases), runs each through a mock agent, and evaluates with `GEvalGenerationEvaluator` (completeness, groundedness, redundancy) & `DeepEvalToolCorrectnessMetric`. Results are saved to `results/`.

   Expected outcome: Cases 1 and 3 fail `completeness` — the mock tool outputs were missing items from the expected response.

4. **(Optional) Run the calibrated evaluation**

   After reviewing the failures, domain experts confirmed the root cause: for multi-item queries, a fixed `expected_output` becomes stale as catalogs change. `eval_calibrated.py` replaces `completeness` with `context_sufficiency` for Cases 1 and 3 — together they attribute failures to the agent layer (wrong tool call) or the tool layer (incomplete data).

   ```bash
   make run-eval-calibrated
   ```

   Cases 1 and 3 now **pass**: `context_sufficiency` confirms the tool output was sufficient to answer the query. The `completeness` failures in `eval.py` were false negatives caused by a stale reference.

## 📊 Evaluation Logic

All scripts use `GEvalGenerationEvaluator` to compare the agent's actual output against the expected output from the CSV. Tool call outputs are treated as `retrieved_context` — the information the agent retrieved to generate its response.

| Metric | What It Measures | Default Threshold |
| --- | --- | --- |
| `completeness` | All key facts from `expected_output` are present in `actual_output` | `1.0` |
| `groundedness` | Every claim in `actual_output` is supported by tool output context | `1.0` |
| `redundancy` | `actual_output` does not contain unnecessary repetition | `0.5` |
| `tool_correctness` | The agent called the right tool with the right arguments | varies |
| `context_sufficiency` | Tool outputs contain enough information to fully answer the query | `1.0` |

`eval_calibrated.py` replaces `completeness` with `tool_correctness` + `context_sufficiency` for multi-item enumeration queries where catalog data may change over time.

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation Evals Lifecycle page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/evals-lifecycle).
