def resolve_base_url(model_id: str) -> str:
    provider = model_id.split("/", 1)[0]
    return f"https://{provider}.example.com/v1"

base_url_binding = Lazy.resolver(resolve_base_url, arg_name="model_id")
