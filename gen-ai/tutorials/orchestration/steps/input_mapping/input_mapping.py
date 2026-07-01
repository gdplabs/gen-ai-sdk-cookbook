from gllm_pipeline.steps import ComponentStep
from gllm_pipeline.types import Val
from gllm_core.schema.component import Component
from typing import Any

class AdvancedProcessor(Component):
    """A component that processes text with various parameters."""

    async def _run(self, **kwargs: Any) -> Any:
        text = kwargs["text"]
        max_length = kwargs["max_length"]
        prefix = kwargs["prefix"]
        suffix = kwargs["suffix"]

        processed = f"{prefix}{text[:max_length]}{suffix}"
        return {"processed_text": processed, "original_length": len(text)}

# Create step with mixed input_map
processor_step = step(
    AdvancedProcessor(),
    input_map={
        "text": "user_input",           # From state
        "max_length": "config_max_len", # From config
        "prefix": Val(">>> "),          # Fixed value
        "suffix": Val(" <<<")           # Fixed value
    },
    output_state=["processed_text", "original_length"]  # Multiple outputs
)

# Create pipeline
pipeline = Pipeline(steps=[processor_step])

# Invoke with state and config
result = await pipeline.invoke(
    initial_state={"user_input": "This is a very long text that will be truncated"},
    config={"configurable": {"config_max_len": 20}}
)

print(result)
# Output: {
#   "user_input": "This is a very long text that will be truncated",
#   "processed_text": ">>> This is a very long <<<",
#   "original_length": 50
# }
