import asyncio

from gllm_core.constants import EventLevel
from gllm_core.event.event_emitter import EventEmitter
from gllm_core.schema.event import Event


async def main() -> None:
    emitter = EventEmitter.with_console_handler(event_level=EventLevel.INFO)

    await emitter.emit(Event(value="Hello, world!", level=EventLevel.INFO))
    await emitter.emit(Event(value="This is a debug message.", level=EventLevel.DEBUG))
    await emitter.emit(Event(value="This is a warning!", level=EventLevel.WARN))
    await emitter.close()


if __name__ == "__main__":
    asyncio.run(main())
