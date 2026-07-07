from gllm_core.schema import Tool, tool


@tool(description="Get weather information")
async def fetch_weather(location: str, units: str = "metric") -> dict:
    """Get weather information for a location.

    Arguments:
        location: City name or query string (e.g. `"Jakarta"`).
        units: Unit system, such as `"metric"` or `"imperial"`.
    """
    # Implementation goes here
    return {"temperature": 22.5, "conditions": "sunny"}


# After decoration, `fetch_weather` is a Tool instance
assert isinstance(fetch_weather, Tool)

# You can call it like a normal function
result = await fetch_weather("New York", "imperial")

# Or use the unified `invoke()` helper
result = await fetch_weather.invoke(location="Tokyo", units="metric")
