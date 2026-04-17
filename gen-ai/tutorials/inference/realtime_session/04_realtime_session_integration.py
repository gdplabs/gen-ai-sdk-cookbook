import asyncio
import json

from dotenv import load_dotenv
from gllm_core.event import EventEmitter
from gllm_core.schema import tool
from gllm_inference.realtime_session import GoogleRealtimeSession
from gllm_inference.realtime_session.input_streamer import EventInputStreamer
from gllm_inference.realtime_session.output_streamer import EventOutputStreamer
from gllm_inference.realtime_session.schema import RealtimeEvent, RealtimeActivityType

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


event_emitter = EventEmitter.with_stream_handler()
input_streamer = EventInputStreamer()
output_streamer = EventOutputStreamer(event_emitter)


async def start_realtime_session():
    """Starts the realtime session module."""
    realtime_session = GoogleRealtimeSession("gemini-2.5-flash-native-audio-preview-12-2025", tools=[get_weather])
    await realtime_session.start(input_streamers=[input_streamer], output_streamers=[output_streamer])

async def stream_output():
    """Streams the output of the realtime session to external systems via event emitter."""
    async for event in event_emitter.stream():
        event_data = json.loads(event)
        if event_data["type"] == "audio":
            event_data["value"] = "<audio_bytes>"
        print(f"Event: {json.dumps(event_data)}")

async def send_text(text: str):
    """Pushes text from the external system to the realtime session via the input streamer."""
    await asyncio.sleep(5)
    input_streamer.push(RealtimeEvent.input_text(text))

async def terminate():
    """Terminates the realtime session via the input streamer."""
    await asyncio.sleep(30)
    input_streamer.push(RealtimeEvent.activity(RealtimeActivityType.TERMINATION))

async def main():
    _ = asyncio.create_task(start_realtime_session())
    _ = asyncio.create_task(stream_output())
    await send_text("Hi, what's the weather in Jakarta?")
    await send_text("While checking the weather, tell me about the history of Indonesia!")
    await terminate()

if __name__ == "__main__":  
    asyncio.run(main())
