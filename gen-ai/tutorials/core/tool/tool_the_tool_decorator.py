from gllm_core.schema import tool


@tool(name="weather", title="Weather Tool")
async def fetch_weather(location: str, units: str = "metric") -> dict:
    ...
