"""Instance caching with DynamicComponent.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/dynamic-component#instance-caching
"""

import asyncio

from gllm_core.schema import Component, DynamicComponent, Lazy, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str) -> str:
        return f"{self.prefix} {name} [{self.model_id}]"


async def main():
    cached_greeter = DynamicComponent(
        component_class=GreetingComponent,
        init_kwargs={"prefix": "Hello", "model_id": Lazy.from_runtime("model_id")},
        cache_instances=True,
        cache_size=256,
    )

    # Equal resolved init kwargs map to the same cached instance
    result1 = await cached_greeter.run(model_id="openai/gpt-4.1-nano", name="Alya")
    result2 = await cached_greeter.run(model_id="openai/gpt-4.1-nano", name="John")
    print(result1)
    print(result2)


if __name__ == "__main__":
    asyncio.run(main())
