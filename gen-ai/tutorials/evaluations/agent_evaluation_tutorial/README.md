# Agent Evaluation Tutorial

This guide shows how to evaluate AI agent trajectories using **gllm-evals**. To perform agent evaluation, use the `AgentEvaluator` to assess agent performance. `AgentEvaluator` combines tool correctness assessment with generation quality evaluation and provides flexible configuration options. Results can also be monitored via Langfuse.

## Quick Start

### 1. Install Dependencies

```bash
make install
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `OPENAI_API_KEY` - OpenAI API Key for evaluation models
- `GOOGLE_API_KEY` - Google API Key for evaluation models

### 3. Run the Examples

```bash
make run                      # Run basic agent evaluation
make run-available-tools     # Run agent evaluation with available tools context
make run-trajectory          # Run agent evaluation with trajectory accuracy
make run-evaluate-helper     # Run agent evaluation with evaluate helper function
```

## Tutorial Contents

### Example 1: Basic Agent Evaluation

**Run:** `make run`

This example demonstrates basic agent evaluation using `AgentEvaluator`:

```python
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator

dataset = load_simple_agent_tool_call_dataset()
evaluator = AgentEvaluator()
result = await evaluator.evaluate(dataset[0])
```

By default, `AgentEvaluator` constructs `DeepEvalToolCorrectnessMetric` and `GEvalGenerationEvaluator` to be used.

The evaluator checks:
- Tool call correctness (compares to reference)
- Parameter accuracy
- Response relevance

**Note:** Without `available_tools`, the evaluator can only assess if the called tools match the expected tools.

### Example 2: Agent Evaluation with Available Tools

**Run:** `make run-available-tools`

This example demonstrates agent evaluation with `available_tools` context. Providing `available_tools` significantly improves evaluation accuracy by evaluating with LLM if the tools provided to the agent are the most fit:

```python
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset, load_tool_schema
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics.agent.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric

# Load tool schema
available_tools = load_tool_schema()

# Configure tool correctness metric with available tools
tool_correctness = DeepEvalToolCorrectnessMetric(
    model=DefaultValues.AGENT_EVALS_MODEL,
    model_credentials=os.getenv("OPENAI_API_KEY"),
    available_tools=available_tools,  # Provide tool context
)

# Create evaluator
evaluator = AgentEvaluator(
    tool_correctness_metric=tool_correctness,
)
```

With `available_tools`, the evaluator can also judge:
- Whether the agent selected the most appropriate tool from available options
- If the agent missed better tool alternatives
- Context-aware reasoning about tool selection

**Tool Schema Format:**
```python
[
    {
        "name": "calculator",
        "description": "Perform mathematical calculations and computations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "weather_search",
        "description": "Get weather information for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get weather for"
                }
            },
            "required": ["location"]
        }
    }
]
```

`DeepEvalToolCorrectnessMetric` returns the lowest score between:
- Tool selection score compared to `available_tools`
- Comparison score between the tool calls and the reference

### Example 3: Agent Evaluation with Trajectory Accuracy

**Run:** `make run-trajectory`

This example demonstrates agent evaluation with trajectory accuracy using `LangChainAgentTrajectoryAccuracyMetric`:

```python
from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics.agent.langchain_agent_trajectory_accuracy import (
    LangChainAgentTrajectoryAccuracyMetric,
)

trajectory_accuracy = LangChainAgentTrajectoryAccuracyMetric(
    model=DefaultValues.AGENT_EVALS_MODEL,
    model_credentials=os.getenv("OPENAI_API_KEY"),
)

evaluator = AgentEvaluator(
    trajectory_accuracy_metric=trajectory_accuracy,
)
```

The trajectory accuracy metric evaluates:
- Agent's full trajectory using LangChain's agentevals approach
- Agent's decision path
- Tool selection correctness
- Sequential reasoning quality

**Note:** The trajectory accuracy metric is **disabled by default** and only runs when `LangChainAgentTrajectoryAccuracyMetric` is provided with `agent_trajectory` and `expected_agent_trajectory` fields in the input data.

**Note:** Agent Trajectory Evaluator will not affect the final score of AgentEvaluator and is purely used to evaluate the trajectory only. Using `LangChainAgentTrajectoryAccuracyMetric` may be costly as it compares the full trajectory to the referenced trajectory.

### Example 4: Using Evaluate Helper Function

**Run:** `make run-evaluate-helper`

This example demonstrates how to use the `evaluate` helper function with `AgentEvaluator` for batch evaluation:

```python
import asyncio
import json
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator

async def main():
    dataset = load_simple_agent_tool_call_dataset()

    async def generate_agent_response(item):
        return {
            "query": item.get("query"),
            "generated_response": item.get("generated_response"),
            "expected_response": item.get("expected_response"),
            "agent_trajectory": item.get("agent_trajectory", []),
            "expected_agent_trajectory": item.get("expected_agent_trajectory", []),
            "tools_called": item.get("tools_called", []),
            "expected_tools": item.get("expected_tools", [])
        }

    results = await evaluate(
        data=dataset,
        inference_fn=generate_agent_response,
        evaluators=[AgentEvaluator()],
    )
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

The `evaluate` helper function provides:
- Batch evaluation over entire datasets
- Automatic result aggregation
- Flexible inference function for generating agent responses
- Support for multiple evaluators

## Data Format

The agent evaluation requires the following input fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | User input/question |
| `generated_response` | string | Yes | Agent's final response |
| `expected_response` | string | Yes | Expected/reference response |
| `tools_called` | array | No | List of tools called by the agent |
| `expected_tools` | array | No | Expected/reference tools |
| `agent_trajectory` | array | No | Agent's full execution path |
| `expected_agent_trajectory` | array | No | Expected reference trajectory |

### Example Dataset Structure (with Tool Calls)

```json
{
  "question_id": "4",
  "query": "Send an email to john@example.com about the meeting",
  "generated_response": "Email sent successfully to jane@example.com",
  "expected_response": "Email has been sent to john@example.com regarding the meeting.",
  "tools_called": [
    {
      "name": "send_email",
      "args": {
        "to": "jane@example.com",
        "subject": "Meeting",
        "body": "This is a reminder about our upcoming meeting."
      },
      "output": "{\"status\": \"sent\"}"
    }
  ],
  "expected_tools": [
    {
      "name": "send_email",
      "args": {
        "to": "john@example.com",
        "subject": "Meeting",
        "body": "This is a reminder about our upcoming meeting."
      },
      "output": "{\"status\": \"sent\"}"
    }
  ]
}
```

### Example Dataset Structure (with Agent Trajectory)

```json
{
  "question_id": "1",
  "query": "What is 15 plus 27?",
  "generated_response": "15 plus 27 equals 42.",
  "expected_response": "15 plus 27 equals 42.",
  "agent_trajectory": [
    {
      "role": "user",
      "content": "What is 15 plus 27?"
    },
    {
      "role": "assistant",
      "content": "",
      "tool_calls": [
        {
          "id": "call_2",
          "type": "function",
          "function": {
            "name": "calculator",
            "arguments": "{\"expression\": \"15 + 27\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_2",
      "content": "42"
    },
    {
      "role": "assistant",
      "content": "15 plus 27 equals 42."
    }
  ],
  "expected_agent_trajectory": [
    {
      "role": "user",
      "content": "What is 15 plus 27?"
    },
    {
      "role": "assistant",
      "content": "",
      "tool_calls": [
        {
          "id": "call_2",
          "type": "function",
          "function": {
            "name": "calculator",
            "arguments": "{\"expression\": \"15 + 27\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_2",
      "content": "42"
    },
    {
      "role": "assistant",
      "content": "15 plus 27 equals 42."
    }
  ]
}
```

## Available Make Commands

```bash
make install              # Install dependencies
make run                  # Run basic agent evaluation
make run-available-tools  # Run agent evaluation with available tools context
make run-trajectory       # Run agent evaluation with trajectory accuracy
make run-evaluate-helper  # Run agent evaluation with evaluate helper function
make clean                # Clean up generated files
```

## Metric Configuration

### DeepEvalToolCorrectnessMetric Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `threshold` | float | 0.5 | Passing threshold between 0-1 |
| `model` | str | - | Model used for evaluation |
| `model_credentials` | str | - | API Key for the model |
| `available_tools` | list[dict] | None | Tools schema/definition available to the agent |
| `strict_mode` | bool | False | If True, scores return as 0 or 1 |
| `should_exact_match` | bool | False | Requires exact match in tool name, args, and output |
| `should_consider_ordering` | bool | False | Consider ordering of tools in evaluation |
| `evaluation_params` | list[str] | ["args", "output"] | Parameters to evaluate in tool calls |
| `include_reason` | bool | True | Include explanation in scoring result |

### LangChainAgentTrajectoryAccuracyMetric Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | - | Model used for evaluation (recommended: gpt-4.1) |
| `model_credentials` | str | - | API Key for the model |
| `use_reference` | bool | True | Compare agent trajectory to expected trajectory |
| `continuous` | bool | False | Return score as float between 0-1 |
| `use_reasoning` | bool | False | Include explanation in output |
| `few_shot_examples` | list[FewShotExample] | None | Few-shot examples for context |

## Further Reading

- [Getting Started](../getting_started/) - Basic evaluation concepts
- [Create Custom Evaluator](../create_custom_evaluator_scorer/) - Custom evaluator guide
- [Multiple LLM-as-a-Judge](../multiple_llm_as_a_judge/) - Using multiple judges
