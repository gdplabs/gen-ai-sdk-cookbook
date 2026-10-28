# Switching the Judge Model

This cookbook evaluates a FAQ chatbot for an online clothing store and switches the model away from the SDK default, `openrouter/deepseek/deepseek-v4.1-flash-1017`: on a metric, on an evaluator, per suite in `evaluate_suites()`, and in YAML suites through one `JUDGE_MODEL` env var.

See the full tutorial: [Tutorial Switch the Judge Model](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model)

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/tutorials/switching_judge_model
   ```

2. **Set UV authentication and install dependencies**

   ```bash
   make sync
   ```

   This will authenticate with Google Cloud and install all dependencies via UV.

3. **Prepare `.env` file**

   Create a file called `.env` in the project root. Every model in this tutorial is served through OpenRouter, so set your OpenRouter key:

   ```env
   OPENROUTER_API_KEY="sk-or-..."
   ```

4. **Run the steps**

   ```bash
   make run-step0   # Run a metric on the default model
   make run-step1   # Switch the model on a metric
   make run-step2   # Switch the model on an evaluator
   make run-step3   # Use a different model per suite with evaluate_suites()
   make run-step4   # Run the YAML suites in suites/
   ```

   Step 1 and Step 2 also have optional scripts:

   ```bash
   make run-step1-multiple   # Step 1: use multiple judges on a metric
   make run-step1-fallback   # Step 1: add a fallback judge to a metric
   make run-step2-per-metric # Step 2: give each metric of an evaluator its own model
   ```

   Each step prints the result. Its `model_id` fields show which model scored each metric.

5. **(Optional) Switch every YAML suite at once**

   The suites in `suites/` default to `openrouter/openai/gpt-6-luna`. To run them on DeepSeek without editing any file, add these lines to `.env` and run Step 4 again. `JUDGE_PROVIDER` pins the OpenRouter provider that serves `JUDGE_MODEL`:

   ```env
   JUDGE_MODEL="openrouter/deepseek/deepseek-v4.1-flash-1017"
   JUDGE_PROVIDER="inference.net"
   ```

   To go back to `openrouter/openai/gpt-6-luna`, delete the lines.

## Project Structure

```
switching_judge_model/
├── suites/                       # YAML suites, model_id: ${JUDGE_MODEL:-openrouter/openai/gpt-6-luna}
│   ├── returns.yaml
│   └── shipping.yaml
├── test_cases.py                 # The FAQ chatbot's test cases
├── step0_default_judge.py
├── step1_metric_judge.py
├── step1_multiple_judges.py
├── step1_fallback_model.py
├── step2_evaluator_judge.py
├── step2_per_metric_models.py
├── step3_suite_judges.py
├── step4_yaml_suites.py
├── pyproject.toml
├── Makefile
└── .env.example
```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook Tutorial Switch the Judge Model page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model).
