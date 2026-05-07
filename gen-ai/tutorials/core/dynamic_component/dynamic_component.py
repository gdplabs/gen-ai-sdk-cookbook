import asyncio

from gllm_core.schema import Component, DynamicComponent, Lazy, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str, tone: str = "casual") -> str:
        return f"{self.prefix} {name}! [model={self.model_id}, tone={tone}]"


async def main_func():
    dynamic_greeter = DynamicComponent(
        component_class=GreetingComponent,
        init_kwargs={
            "prefix": "Hello",
            "model_id": Lazy.from_runtime("model_id"),
        },
    )

    result = await dynamic_greeter.run(
        model_id="openai/gpt-4.1-nano",
        name="John Doe",
        tone="formal",
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main_func())
