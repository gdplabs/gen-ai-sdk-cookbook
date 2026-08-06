from gllm_core.schema import Component, Lazy, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str, tone: str = "casual") -> str:
        return f"{self.prefix} {name}! [model={self.model_id}, tone={tone}]"


dynamic_greeter = GreetingComponent.to_dynamic(
    init_kwargs={
        "prefix": "Hi",
        "model_id": Lazy.from_runtime("model_id"),
    },
)

result = await dynamic_greeter.run(
    model_id="openai/gpt-4.1-nano",
    name="Alya",
    tone="friendly",
)
