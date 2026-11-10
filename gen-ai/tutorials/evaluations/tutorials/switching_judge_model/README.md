# Switching the Judge Model

This cookbook evaluates a FAQ chatbot for an online clothing store and switches the judge model away from the SDK default, DeepSeek (`openrouter/deepseek/deepseek-v4.1-flash-1017`): on a metric, on an evaluator, per suite in `evaluate_suites()`, and in YAML suites through one `JUDGE_MODEL` env var. Every model goes through OpenRouter, so one `OPENROUTER_API_KEY` runs the whole tutorial.

See the full tutorial: [Tutorial Switch the Judge Model](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model)

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/tutorials/switching_judge_model
   ```

2. **Install dependencies**

   ```bash
   make sync
   ```

   This installs all dependencies from PyPI via UV.

3. **Prepare `.env` file**

   Create a file called `.env` in the project root. This tutorial calls every model through OpenRouter, so your OpenRouter key is the only setting you need:

   ```env
   OPENROUTER_API_KEY="sk-or-..."
   ```

4. **Run a level**

   Each level is independent. Run the one you need:

   ```bash
   make run-default    # Run a metric on the default judge, DeepSeek, set explicitly
   make run-metric     # Switch the judge on a metric
   make run-evaluator  # Switch the judge on an evaluator
   make run-suite      # Use different judges per suite with evaluate_suites()
   make run-yaml       # Run the YAML suites in suites/
   ```

   The metric and evaluator levels also have optional scripts:

   ```bash
   make run-metric-multiple       # Use multiple judges on a metric
   make run-metric-fallback       # Add a fallback judge to a metric
   make run-evaluator-per-metric  # Give each metric of an evaluator its own judge
   ```

   Run `make run-all` to run every level. Each script prints the result as a dict. Its `model_id` fields show which model scored each metric.

5. **(Optional) Switch every YAML suite at once**

   The suites in `suites/` default to `openrouter/openai/gpt-6-luna`. To run them on DeepSeek without editing any file, add these lines to `.env` and run `make run-yaml` again. `JUDGE_PROVIDER` pins the OpenRouter provider that serves `JUDGE_MODEL`:

   ```env
   JUDGE_MODEL="openrouter/deepseek/deepseek-v4.1-flash-1017"
   JUDGE_PROVIDER="inference-net"
   ```

   To go back to `openrouter/openai/gpt-6-luna`, delete the lines.

## Project Structure

```
switching_judge_model/
├── suites/                          # YAML suites, model_id: ${JUDGE_MODEL:-openrouter/openai/gpt-6-luna}
│   ├── returns.yaml
│   └── shipping.yaml
├── test_cases.py                    # The FAQ chatbot's test cases
├── default_judge.py
├── metric_judge.py
├── metric_multiple_judges.py
├── metric_fallback_model.py
├── evaluator_judge.py
├── evaluator_per_metric_models.py
├── suite_judges.py
├── yaml_suites.py
├── pyproject.toml
├── Makefile
└── .env.example
```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook Tutorial Switch the Judge Model page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model).
