# Evaluate Agent Q&A Responses

This guide will walk you through evaluating a single agent's response using the GL SDK evaluation module. You'll learn how to measure the accuracy and completeness of an agent's answer against a predefined expected output.

## The Usecase: Knowledgeable Assistant

In this example, we evaluate a simple "Knowledgeable Assistant" agent. We want to ensure that when asked a factual question (like the capital of France), the agent provides a direct, accurate, and non-redundant response.

## 🚀 Getting Started

To follow along with this tutorial, we will use the code from the **Agent QnA Evaluations** cookbook.

{% stepper %}
{% step %}
**Clone the repository & open the directory**

```bash
git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gen-ai/examples/evaluations/agent_qna_evaluations
```
{% endstep %}

{% step %}
**Install dependencies using UV**

Run the following command to sync your environment:

```bash
make sync
```
{% endstep %}

{% step %}
**Prepare your `.env` file**

Create a file called `.env` in the project root based on the template:

```bash
cp .env.example .env
```

Edit the `.env` file and set your API keys:
```env
GOOGLE_API_KEY="AIza..."
```
{% endstep %}
{% endstepper %}

***

## 1) Agent Usage Pattern

Before diving into evaluation, it's important to understand how the agent is initialized and run locally using the GL SDK. Unlike remote agents, local agents do not require deployment to the AIP platform.

{% code title="main.py" lineNumbers="true" %}
```python
from glaip_sdk.agents import Agent

# Create and run locally (no deploy needed)
hello_agent = Agent(
    name="hello_local_agent",
    instruction="You are a knowledgeable assistant.",
)

# Runs immediately on your machine
response = hello_agent.run("whats the capital of france ?")
```
{% endcode %}

***

## 2) Customize the Evaluation

The core logic resides in `main.py`. To evaluate different questions or scenarios, you can modify the following sections.

### Define your Test Case

In `main.py`, you can modify the `QUERY` and `EXPECTED_OUTPUT` constants. The evaluator uses these to compare what the agent *actually* says against what it *should* have said.

{% code title="main.py" lineNumbers="true" %}
```python
# 💡 MODIFY THESE for your specific test case
QUERY = "whats the capital of france ?"
EXPECTED_OUTPUT = "The capital of France is Paris."
```
{% endcode %}

### Choose your Judge Model

The evaluation uses a "Judge" model (LLM-as-a-judge) to perform the scoring. By default, it uses Gemini, but you can switch to any supported model.

{% code title="main.py" lineNumbers="true" %}
```python
# 💡 MODIFY the model ID to use a different judge
judge_model = build_lm_invoker(
    "google/gemini-3-flash-preview", # You can use gpt-4o, etc.
    os.getenv("GOOGLE_API_KEY"),
)
evaluator = GEvalGenerationEvaluator(models=judge_model)
```
{% endcode %}

***

## 3) Run & Analyze

{% stepper %}
{% step %}
**Execute the evaluation**

Run the following command to execute the agent and trigger the evaluation process:

```bash
uv run python main.py
```
{% endstep %}

{% step %}
**Observe the Evaluation Result**

The output will show the agent's response followed by the evaluation metrics:

```json
{
  "generation": {
    "aggregate_explanation": "All metrics met the expected values.",
    "aggregate_success": true,
    "aggregate_score": 1.0,
    "completeness": {
      "score": 1.0,
      "explanation": "The minimum key facts are: [A] Paris. The Generated Response correctly identifies 'Paris' as the answer...",
      "success": true,
      "threshold": 1.0,
      "model_id": "google/gemini-3-flash-preview"
    },
    "redundancy": {
      "score": 0.0,
      "explanation": "The response is extremely concise, consisting of a single word that directly answers the question...",
      "success": true,
      "threshold": 0.5,
      "model_id": "google/gemini-3-flash-preview"
    }
  }
}
```

The metrics measured include:
- **Completeness**: Checks if all key facts from the expected output are present.
- **Redundancy**: Checks if the response contains unnecessary repetition.
{% endstep %}
{% endstepper %}

***

## Key Customization Tips

* **configuration**: You can adjust the evals configuration such as models in the evaluator configuration.
* **Agent Configuration**: You can modify the `Agent` instruction in `main.py` to see how it affects the evaluation scores (e.g., tell it to be "very verbose" and watch the **Redundancy** score change).
