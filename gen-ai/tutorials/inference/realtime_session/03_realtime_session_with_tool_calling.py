import asyncio

from dotenv import load_dotenv
from gllm_core.schema import tool
from gllm_inference.realtime_session import GoogleRealtimeSession
from gllm_inference.realtime_session.input_streamer import KeyboardInputStreamer, LinuxMicInputStreamer
from gllm_inference.realtime_session.output_streamer import ConsoleOutputStreamer, LinuxSpeakerOutputStreamer

load_dotenv()


@tool
async def get_weather(city: str) -> str:
    """Get the weather of a city.
    
    Args:
        city (str): The city to get the weather of.

    Returns:
        str: The weather of the city.
    """
    await asyncio.sleep(15)  # Simulate a long-running task
    return f"{city} weather: cloudy, 23°C."


input_streamers = [KeyboardInputStreamer(), LinuxMicInputStreamer()]
output_streamers = [ConsoleOutputStreamer(), LinuxSpeakerOutputStreamer()]


async def main():
    realtime_session = GoogleRealtimeSession("gemini-2.5-flash-native-audio-preview-12-2025", tools=[get_weather])
    await realtime_session.start(input_streamers=input_streamers, output_streamers=output_streamers)


if __name__ == "__main__":
    asyncio.run(main())
