from gllm_core.schema import DynamicComponent, Lazy
from gllm_core.schema import Component, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str) -> str:
        return f"{self.prefix} {name} [{self.model_id}]"


cached_greeter = DynamicComponent(
    component_class=GreetingComponent,
    init_kwargs={"prefix": "Hello", "model_id": Lazy.from_runtime("model_id")},
    cache_instances=True,
    cache_size=256,
)
