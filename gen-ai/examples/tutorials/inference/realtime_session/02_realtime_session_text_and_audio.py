import asyncio

from dotenv import load_dotenv
from gllm_inference.realtime_session import GoogleRealtimeSession
from gllm_inference.realtime_session.input_streamer import KeyboardInputStreamer, LinuxMicInputStreamer
from gllm_inference.realtime_session.output_streamer import ConsoleOutputStreamer, LinuxSpeakerOutputStreamer

load_dotenv()


input_streamers = [KeyboardInputStreamer(), LinuxMicInputStreamer()]
output_streamers = [ConsoleOutputStreamer(), LinuxSpeakerOutputStreamer()]


async def main():
    realtime_session = GoogleRealtimeSession("gemini-2.5-flash-native-audio-preview-12-2025")
    await realtime_session.start(input_streamers=input_streamers, output_streamers=output_streamers)


if __name__ == "__main__":
    asyncio.run(main())
