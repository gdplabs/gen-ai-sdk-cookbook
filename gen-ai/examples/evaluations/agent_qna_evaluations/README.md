# Agent QnA Evaluations

This example demonstrates how to evaluate a single agent's response using the GL SDK evaluation module.

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

3. **Run the evaluation**
   
   ```bash
   make run
   ```

## 📊 Evaluation Logic

The evaluation uses `GEvalGenerationEvaluator` to compare the agent's actual output against an `EXPECTED_OUTPUT` for a given `QUERY`.

You can customize the test case in `main.py`:

```python
QUERY = "whats the capital of france ?"
EXPECTED_OUTPUT = "The capital of France is Paris."
```

The evaluator uses a "Judge" model (e.g., `google/gemini-3-flash-preview`) to score the response.
