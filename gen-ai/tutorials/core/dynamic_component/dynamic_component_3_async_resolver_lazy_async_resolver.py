async def load_api_key(model_id: str) -> str:
    provider = model_id.split("/", 1)[0]
    return f"key-{provider}"

api_key_binding = Lazy.async_resolver(load_api_key, arg_name="model_id")
