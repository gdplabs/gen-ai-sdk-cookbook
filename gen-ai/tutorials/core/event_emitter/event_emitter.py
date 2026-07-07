import asyncio
from gllm_core.event.event_emitter import EventEmitter


async def producer(emitter: EventEmitter) -> None:
    from gllm_core.schema.event import Event
    await emitter.emit(Event(value="Hello, world!"))


async def main() -> None:
    emitter = EventEmitter.with_stream_handler()

    asyncio.create_task(producer(emitter))

    async for event in emitter.stream():
        print("Received:", event)


asyncio.run(main())
