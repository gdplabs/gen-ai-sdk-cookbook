from dotenv import load_dotenv
load_dotenv()

import asyncio
import json

from gllm_core.event import EventEmitter
from gllm_inference.realtime_session import GoogleRealtimeSession
from gllm_inference.realtime_session.input_streamer import EventInputStreamer
from gllm_inference.realtime_session.output_streamer import EventOutputStreamer
from gllm_inference.realtime_session.schema import RealtimeEvent, RealtimeActivityType

event_emitter = EventEmitter.with_stream_handler()
input_streamer = EventInputStreamer()
output_streamer = EventOutputStreamer(event_emitter)

async def start_realtime_session():
    realtime_session = GoogleRealtimeSession("gemini-2.5-flash-native-audio-preview-12-2025")
    await realtime_session.start(input_streamers=[input_streamer], output_streamers=[output_streamer])

async def stream_output():
    async for event in event_emitter.stream():
        data = json.loads(event)

        if data["type"] == "audio":
            data["value"] = "<audio_bytes>"

        print(f"Event: {json.dumps(data)}")

async def send_text(text: str):
    await asyncio.sleep(5)
    input_streamer.push(RealtimeEvent.input_text(text))

async def terminate():
    await asyncio.sleep(5)
    input_streamer.push(RealtimeEvent.activity(RealtimeActivityType.TERMINATION))

async def main():
    asyncio.create_task(start_realtime_session())
    asyncio.create_task(stream_output())
    await send_text("Hi, how are you?")
    await send_text("Tell me about the history of Indonesia!")
    await send_text("Ok stop! That is enough!")
    await terminate()

if __name__ == "__main__":
    asyncio.run(main())
