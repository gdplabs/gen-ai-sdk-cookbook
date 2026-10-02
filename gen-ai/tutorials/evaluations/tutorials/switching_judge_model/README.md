# Switching the Judge Model

This cookbook evaluates a FAQ chatbot for an online clothing store and switches the judge model away from the SDK default, `google/gemini-3.1-flash-lite`: on a metric, on an evaluator, per suite in `evaluate_suites()`, and in YAML suites through one `JUDGE_MODEL` env var.

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
    Create a file called `.env`, then set the API keys for the judge models. The examples use OpenAI and Gemini judges.
    ```env
    OPENAI_API_KEY="..."
    GOOGLE_API_KEY="..."
    ```

4. **Run the steps**

   ```bash
   make run-step0   # Run a metric on the default judge
   make run-step1   # Switch the judge on a metric: one judge, a panel, and a fallback
   make run-step2   # Switch the judge on an evaluator, and give each metric its own judge
   make run-step3   # Use a different judge per suite with evaluate_suites()
   make run-step4   # Run the YAML suites in suites/
   ```

   Each step prints the result. Its `model_id` fields show which judge scored each metric.

5. **(Optional) Switch every YAML suite at once**

   The suites in `suites/` default to `openai/gpt-4o`. To run them on Gemini without editing any file, add this line to `.env` and run Step 4 again:

   ```env
   JUDGE_MODEL="google/gemini-3.1-flash-lite"
   ```

   To go back to `openai/gpt-4o`, delete the line.

> **Only have `OPENAI_API_KEY`?** Every judge call that goes to Gemini fails with an `InvokerRuntimeError` ("No API key was provided"):
>
> - Step 0 stops with that error, because the default judge is Gemini.
> - In Step 1, the panel still scores with GPT, and the Gemini judge's error shows up in `individual_judge_results`.
> - In the "per metric" example of Step 2 and the shipping suite of Step 3, groundedness gets `score=0.0` with the error in its `explanation`, so the evaluator fails. That `0.0` is a missing key, not the judge's verdict.
> - Step 4 with `JUDGE_MODEL="google/gemini-3.1-flash-lite"` fails every metric the same way.
>
> Everything judged only by GPT runs normally, including Step 4 with its default judge.

## Project Structure

```
switching_judge_model/
├── suites/                       # YAML suites, model_id: ${JUDGE_MODEL:-openai/gpt-4o}
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
