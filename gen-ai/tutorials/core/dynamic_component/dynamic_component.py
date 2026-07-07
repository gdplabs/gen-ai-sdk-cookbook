from gllm_core.schema import Component, DynamicComponent, Lazy, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str, tone: str = "casual") -> str:
        return f"{self.prefix} {name}! [model={self.model_id}, tone={tone}]"


dynamic_greeter = DynamicComponent(
    component_class=GreetingComponent,
    init_kwargs={
        "prefix": "Hello",
        "model_id": Lazy.from_runtime("model_id"),
    },
)

result = await dynamic_greeter.run(
    model_id="openai/gpt-4.1-nano",   # consumed by constructor binding
    name="John Doe",                  # passed to @main method
    tone="formal",                    # passed to @main method
)
print(result)
