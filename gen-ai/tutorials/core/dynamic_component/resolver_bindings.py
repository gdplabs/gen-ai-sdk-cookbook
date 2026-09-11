"""Lazy.resolver (sync) and Lazy.async_resolver (async) bindings.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/dynamic-component#2-sync-resolver-lazyresolver
    [2] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/dynamic-component#3-async-resolver-lazyasyncresolver
"""

import asyncio

from gllm_core.schema import Component, DynamicComponent, Lazy, main


class ClientComponent(Component):
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    @main
    async def describe(self) -> str:
        return f"base_url={self.base_url}, api_key={self.api_key}"


def resolve_base_url(model_id: str) -> str:
    """Sync resolver: derive a base URL from the runtime model_id."""
    provider = model_id.split("/", 1)[0]
    return f"https://{provider}.example.com/v1"


async def load_api_key(model_id: str) -> str:
    """Async resolver: simulate an awaited secret lookup."""
    provider = model_id.split("/", 1)[0]
    return f"key-{provider}"


async def main() -> None:
    """Bind a sync and an async resolver as init kwargs, then resolve at runtime."""
    base_url_binding = Lazy.resolver(resolve_base_url, arg_name="model_id")
    api_key_binding = Lazy.async_resolver(load_api_key, arg_name="model_id")

    client = DynamicComponent(
        component_class=ClientComponent,
        init_kwargs={"base_url": base_url_binding, "api_key": api_key_binding},
    )

    result = await client.run(model_id="openai/gpt-4.1-nano")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
