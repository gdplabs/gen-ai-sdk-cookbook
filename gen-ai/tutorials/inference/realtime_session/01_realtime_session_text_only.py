import asyncio

from dotenv import load_dotenv
from gllm_inference.realtime_session import GoogleRealtimeSession

load_dotenv()


async def main():
    realtime_session = GoogleRealtimeSession("gemini-2.5-flash-native-audio-preview-12-2025")
    await realtime_session.start()


if __name__ == "__main__":
    asyncio.run(main())
