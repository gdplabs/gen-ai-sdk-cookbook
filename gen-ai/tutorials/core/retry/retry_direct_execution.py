from gllm_core.retry import retry, RetryConfig


async def unreliable_call(user_id: str) -> dict:
    # May raise transient errors
    return await api.get_user(user_id)


config = RetryConfig(max_retries=2, base_delay=0.5)
result = await retry(unreliable_call, "user_123", retry_config=config)
