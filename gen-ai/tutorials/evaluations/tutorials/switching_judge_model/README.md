# Switching the Judge Model

This cookbook evaluates a FAQ chatbot for an online clothing store and switches the model away from the SDK default, `google/gemini-3.1-flash-lite`: on a metric, on an evaluator, per suite in `evaluate_suites()`, and in YAML suites through one `JUDGE_MODEL` env var.

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

   Create a file called `.env` in the project root. This tutorial uses OpenAI, OpenRouter, and Gemini models on Vertex AI, so set your OpenAI key, your OpenRouter key, and your Vertex AI settings:

   ```env
   OPENAI_API_KEY="sk-..."
   OPENROUTER_API_KEY="sk-or-..."
   # the path to your service account JSON file
   GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
   # the Vertex AI location
   GOOGLE_CLOUD_LOCATION=global
   # the labels added to every Vertex AI call, as a JSON object, for usage tracking only
   GOOGLE_VERTEX_LABEL={"organization": "<your_org>", "project_name": "<project_name>", "environment": "<environment>"}
   ```

4. **Run the steps**

   ```bash
   make run-step0   # Run a metric on the default model
   make run-step1   # Switch the model on a metric: one model, multiple judges, and a fallback
   make run-step2   # Switch the model on an evaluator, and give each metric its own model
   make run-step3   # Use a different model per suite with evaluate_suites()
   make run-step4   # Run the YAML suites in suites/
   ```

   Each step prints the result. Its `model_id` fields show which model scored each metric.

5. **(Optional) Switch every YAML suite at once**

   The suites in `suites/` default to `openai/gpt-6-luna`. To run them on Gemini without editing any file, add this line to `.env` and run Step 4 again:

   ```env
   JUDGE_MODEL="google/gemini-3.1-flash-lite"
   ```

   To go back to `openai/gpt-6-luna`, delete the line.

> **No `GOOGLE_APPLICATION_CREDENTIALS`?** You need it set up to run Step 0, because the default model is a Gemini model on Vertex AI.

## Project Structure

```
switching_judge_model/
├── suites/                       # YAML suites, model_id: ${JUDGE_MODEL:-openai/gpt-6-luna}
│   ├── returns.yaml
│   └── shipping.yaml
├── test_cases.py                 # The FAQ chatbot's test cases
├── step0_default_judge.py
├── step1_metric_judge.py
├── step2_evaluator_judge.py
├── step3_suite_judges.py
├── step4_yaml_suites.py
├── pyproject.toml
├── Makefile
└── .env.example
```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook Tutorial Switch the Judge Model page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model).
