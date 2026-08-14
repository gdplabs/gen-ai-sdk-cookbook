"""Persist pipeline checkpoints to a datastore instead of memory.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/observability-and-debugging#durable-checkpointing-with-datastoresaver
"""

import asyncio
from typing import TypedDict

from gllm_datastore.data_store.in_memory.data_store import InMemoryDataStore
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class DummyState(TypedDict):
    text: str
    text_upper: str


def to_upper(data: dict) -> str:
    return data["text"].upper()


async def main() -> None:
    """Runs the same history operations as state_history.py, backed by a datastore."""
    # Swap InMemoryDataStore for a persistent BaseDataStore in production.
    data_store = InMemoryDataStore()

    # Pass a BaseDataStore directly; Pipeline auto-wraps it in a DataStoreSaver.
    pipeline = Pipeline(
        steps=[
            transform(
                to_upper,
                input_map=["text"],
                output_state="text_upper",
                name="to_upper",
            )
        ],
        state_type=DummyState,
        checkpointer=data_store,
    )
    await pipeline.invoke({"text": "hello", "text_upper": ""}, thread_id="t1")

    print("State history for t1 (read from the datastore):")
    async for snapshot in pipeline.get_state_history("t1"):
        print(snapshot.values)

    await pipeline.checkpointer.adelete_thread("t1")
    print("Thread t1 deleted from the datastore.")


if __name__ == "__main__":
    asyncio.run(main())
