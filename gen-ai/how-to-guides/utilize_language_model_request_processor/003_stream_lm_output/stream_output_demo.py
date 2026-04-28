"""Runnable example for streaming LM output through Event objects."""

import asyncio
import logging

from gllm_core.constants import EventType
from gllm_core.event import EventEmitter
from gllm_core.event.handler.event_handler import BaseEventHandler
from gllm_core.schema import Event

from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import LMOutput, Message, ModelId


class RecordingEventHandler(BaseEventHandler):
    def __init__(self) -> None:
        super().__init__(name="RecordingEventHandler")
        self.events: list[Event] = []

    async def emit(self, event: Event) -> None:
        self.events.append(event)


class StreamingDemoInvoker(BaseLMInvoker):
    async def _invoke(self, messages, config, transformer, stream) -> LMOutput:
        del config, messages
        chunks = ["Luminafox ", "glows ", "through ", "the ", "forest."]

        if stream and transformer:
            await transformer.emit(Event(type=EventType.STATUS, value="Starting response stream"))
            for chunk in chunks:
                await asyncio.sleep(0)
                await transformer.emit(Event(type=EventType.RESPONSE, value=chunk))
            await transformer.emit(Event(type=EventType.STATUS, value="Stream completed"))

        output = LMOutput()
        output.add_text("".join(chunks))
        return output

    def _format_messages(self, messages: list[Message]) -> list[Message]:
        return messages


async def main() -> None:
    logging.disable(logging.CRITICAL)

    handler = RecordingEventHandler()
    event_emitter = EventEmitter(handlers=[handler])
    invoker = StreamingDemoInvoker(model_id=ModelId.from_string("openai/gpt-5-nano"))
    processor = LMRequestProcessor(
        PromptBuilder(
            system_template="Stream your answer in short response chunks.",
            user_template="{query}",
        ),
        invoker,
    )

    result = await processor.process(
        query="Describe the glowing forest creature.",
        event_emitter=event_emitter,
    )

    print("Captured events")
    for index, event in enumerate(handler.events, start=1):
        print(f"{index}. {event.type}: {event.value}")
    print("Final text")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
