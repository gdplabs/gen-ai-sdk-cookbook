import asyncio
import os

from gllm_evals.dataset.simple_agent_tool_call_dataset import (
    load_simple_agent_tool_call_dataset,
    load_tool_schema,
)
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import (
    DeepEvalToolCorrectnessMetric,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run agent evaluation with available tools context.

    Loads the tool schema and dataset, configures the tool correctness metric
    with available tools context, and evaluates the dataset item.
    """
    # Load tool schema - defines tools available to the agent
    available_tools = load_tool_schema("./dataset_examples")

    # Configure tool correctness metric with available tools
    # With available_tools, the evaluator can judge:
    # - Whether the agent selected the most appropriate tool
    # - If the agent missed better tool alternatives
    # - Context-aware reasoning about tool selection
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )
    tool_correctness = DeepEvalToolCorrectnessMetric(
        models=model,
        available_tools=available_tools,  # Provide tool context
    )

    # Create evaluator
    evaluator = CompositeEvaluator(
        name="agent",
        metrics=[
            tool_correctness,
            GEvalCompletenessMetric(models=model),
            GEvalGroundednessMetric(models=model),
            GEvalRedundancyMetric(models=model),
        ],
    )
    dataset = load_simple_agent_tool_call_dataset("./dataset_examples").load()
    result = await evaluator.evaluate(dataset[2])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
