"""Runnable example for durable human-in-the-loop checkpointing with DataStoreSaver.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#2-running-with-session-persistence
"""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_datastore.data_store.in_memory import InMemoryDataStore
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import if_else, interrupt, step
from langgraph.types import Command


class PipelineState(TypedDict, total=False):
    topic: str
    email_draft: str
    hitl_decision: bool
    email_status: str


class GenerateDraftComponent(Component):
    @main
    async def run(self, topic: str) -> str:
        return f"Draft about: {topic}"


class SendEmailComponent(Component):
    @main
    async def run(self, body: str) -> str:
        return f"Sent: {body}"


class DiscardDraftComponent(Component):
    @main
    async def run(self) -> str:
        return "Draft discarded"


def build_pipeline(data_store: InMemoryDataStore) -> Pipeline:
    """Builds the HITL pipeline with a DataStoreSaver-backed checkpointer."""
    draft_email = step(
        GenerateDraftComponent(),
        output_state="email_draft",
        input_map={"topic": "topic"},
        name="draft_email",
    )
    send_email = step(
        SendEmailComponent(),
        output_state="email_status",
        input_map={"body": "email_draft"},
        name="send_email",
    )
    discard_draft = step(
        DiscardDraftComponent(),
        output_state="email_status",
        name="discard_draft",
    )
    conditional_send = if_else(
        condition=lambda state: state.get("hitl_decision", False),
        if_branch=send_email,
        else_branch=discard_draft,
        name="handle_decision",
    )

    return Pipeline(
        steps=[
            draft_email,
            interrupt(
                name="wait_for_human",
                message={"alert": "Please review the email draft", "priority": "high"},
                resume_value_map="hitl_decision",
            ),
            conditional_send,
        ],
        state_type=PipelineState,
        # Pass a BaseDataStore directly; Pipeline auto-wraps it in a DataStoreSaver.
        checkpointer=data_store,
        name="hitl_durable_demo",
    )


async def main() -> None:
    """Pauses and resumes a HITL pipeline with checkpoints in a datastore."""
    # Swap InMemoryDataStore for a persistent BaseDataStore in production.
    data_store = InMemoryDataStore()
    pipeline = build_pipeline(data_store)
    thread_id = "email-session-durable"
    config = {"thread_id": thread_id}

    paused_state = await pipeline.invoke(
        {"topic": "Quarterly earnings report"}, config=config
    )
    print(f"Paused draft: {paused_state['email_draft']}")

    snapshot = await pipeline.get_state(thread_id)
    print(f"Next node: {snapshot.next}")

    final_state = await pipeline.invoke(Command(resume=True), config=config)
    print(f"Final status: {final_state['email_status']}")

    await pipeline.checkpointer.adelete_thread(thread_id)
    print("Thread deleted from the datastore.")


if __name__ == "__main__":
    asyncio.run(main())
