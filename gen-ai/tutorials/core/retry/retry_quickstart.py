from gllm_core.retry import retry


@retry()
async def fetch_data(url: str) -> dict:
    # Simulate an unreliable API call
    response = await make_http_request(url)
    return response.json()
