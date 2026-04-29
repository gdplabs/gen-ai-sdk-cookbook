"""FastAPI server for running the demo pipeline."""

import asyncio

from gllm_core.constants import EventLevel, EventType
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from gllm_core.event import EventEmitter
from gllm_core.event.handler import StreamEventHandler
from gllm_core.schema import Event

from pipeline import e2e_pipeline

app = FastAPI()


async def run_pipeline(state: dict, top_k: int, event_emitter: EventEmitter) -> None:
    try:
        await event_emitter.emit(Event(value="Starting pipeline", level=EventLevel.INFO, type=EventType.STATUS.value))
        result = await e2e_pipeline.invoke(state, context={"top_k": top_k})
        await event_emitter.emit(Event(value=result["response"], level=EventLevel.INFO, type=EventType.RESPONSE.value))
    except Exception as error:
        await event_emitter.emit(Event(value=str(error), level=EventLevel.ERROR, type=EventType.STATUS.value))
    finally:
        await event_emitter.emit(Event(value="Finished pipeline", level=EventLevel.INFO, type=EventType.STATUS.value))
        await event_emitter.close()


@app.post("/stream")
async def add_message(request: Request):
    body = await request.json()
    stream_handler = StreamEventHandler()
    event_emitter = EventEmitter([stream_handler], EventLevel.INFO)

    state = {"user_query": body.get("user_query", "")}
    top_k = body.get("top_k", 3)

    asyncio.create_task(run_pipeline(state, top_k, event_emitter))
    return StreamingResponse(stream_handler.stream(), media_type="application/json")
