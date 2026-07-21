"""State history inspection with get_state_history and forking.

See https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/debug-a-pipeline#state-history
and https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/debug-a-pipeline#forking-from-a-previous-state
"""

import asyncio
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import transform


class HistoryState(TypedDict):
    text: str
    text_upper: str


def to_upper(data: dict) -> str:
    return data["text"].upper()


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            transform(
                to_upper,
                input_map=["text"],
                output_state="text_upper",
                name="to_upper",
            )
        ],
        state_type=HistoryState,
        checkpointer=InMemorySaver(),
    )


async def main() -> None:
    pipeline = build_pipeline()

    # Run twice on the same thread to create checkpoints
    await pipeline.invoke({"text": "hello", "text_upper": ""}, thread_id="thread-1")
    await pipeline.invoke({"text": "world", "text_upper": ""}, thread_id="thread-1")

    # Iterate through checkpointed states (newest first)
    async for snapshot in pipeline.get_state_history("thread-1"):
        print(snapshot.values)

    # Fork from the most recent checkpoint
    history = [snap async for snap in pipeline.get_state_history("thread-1")]
    checkpoint_id = history[0].config["configurable"]["checkpoint_id"]

    new_config = pipeline.fork_from(
        thread_id="thread-1",
        checkpoint_id=checkpoint_id,
        values={"text": "modified input"},
    )

    forked_result = await pipeline.invoke(None, config=new_config)
    print(forked_result)


if __name__ == "__main__":
    asyncio.run(main())
