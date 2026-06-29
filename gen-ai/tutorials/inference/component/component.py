import asyncio
from gllm_inference.component import GenericLMComponent

component = GenericLMComponent.from_config(
    model_id="openai/gpt-5.4-nano",
    system_template="You are a helpful assistant.",
)

output = asyncio.run(component.run(query="What is the capital of France?"))
print(output.text)
