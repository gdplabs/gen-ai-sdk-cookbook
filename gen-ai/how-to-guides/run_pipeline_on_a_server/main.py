"""Main entry point for the FastAPI application.

This module sets up a FastAPI server that exposes your RAG pipeline
through HTTP endpoints with streaming response capabilities.
"""

import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from gllm_core.constants import EventLevel
from gllm_core.event import EventEmitter
from gllm_core.event.handler import ConsoleEventHandler, StreamEventHandler

from pipeline import e2e_pipeline

app = FastAPI()


async def run_pipeline(state: dict, config: dict):
    """Runs the end-to-end pipeline.

    Args:
        state (dict): The state dictionary containing input data and event emitters.
        config (dict): The configuration dictionary containing pipeline parameters.
    """
    event_emitter: EventEmitter = state.get("event_emitter")
    try:
        await event_emitter.emit("Starting pipeline")
        await e2e_pipeline.invoke(state, config)
    except Exception as error:
        await event_emitter.emit(str(error))
    finally:
        await event_emitter.emit("Finished pipeline")
        await event_emitter.close()


@app.post("/stream")
async def add_message(request: Request):
    """Endpoint to handle incoming requests and stream responses.

    Args:
        request (Request): The incoming request containing user query and parameters.

    Returns:
        StreamingResponse: A streaming response that emits events during pipeline execution.
    """
    body = await request.json()
    user_query = body.get("user_query")
    top_k = body.get("top_k")
    debug = body.get("debug", False)
    event_level = EventLevel.DEBUG if debug else EventLevel.INFO

    stream_handler = StreamEventHandler()
    console_handler = ConsoleEventHandler()
    event_emitter = EventEmitter([stream_handler, console_handler], event_level)
    state = {"user_query": user_query, "event_emitter": event_emitter}
    config = {"top_k": top_k}

    asyncio.create_task(run_pipeline(state, config))
    return StreamingResponse(stream_handler.stream())
