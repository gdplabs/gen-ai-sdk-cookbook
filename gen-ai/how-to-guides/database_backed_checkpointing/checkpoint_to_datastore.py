"""Persist pipeline checkpoints to a gllm-datastore BaseDataStore via DataStoreSaver.

Demonstrates the database-backed checkpointing guide end-to-end:

  1. Build a durable human-in-the-loop Pipeline backed by an ``InMemoryDataStore``
     wrapped in a ``DataStoreSaver`` (the ``checkpointer=`` argument accepts either a
     raw ``BaseDataStore`` or an explicit ``DataStoreSaver``).
  2. Invoke the pipeline until it pauses at an ``interrupt`` step, then resume it from
     the same ``thread_id`` — the paused state lives in the datastore, so it survives a
     separate process or worker.
  3. Inspect the persisted history with ``get_state_history`` and fork a what-if branch
     with ``fork_from``.
  4. Delete the thread's checkpoints from the datastore when it is resolved.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/database-backed-checkpointing
"""

from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_datastore.data_store.in_memory.data_store import InMemoryDataStore
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.pipeline.checkpoint import DataStoreSaver
from gllm_pipeline.steps import interrupt, step
from langgraph.types import Command


class ApprovalState(TypedDict, total=False):
    """State shared across the approval pipeline."""

    topic: str
    draft: str
    approved: bool


class DraftComponent(Component):
    """Produces a draft document for a given topic."""

    @main
    async def run(self, topic: str) -> str:
        return f"Draft about: {topic}"


def build_pipeline() -> Pipeline:
    """Return a Pipeline whose checkpoints are stored in an in-memory datastore."""
    data_store = InMemoryDataStore()
    # Option B: construct the saver explicitly to control the namespace.
    # Option A would pass ``data_store`` straight into ``checkpointer=`` and let
    # Pipeline wrap it. Both paths are equivalent.
    saver = DataStoreSaver(data_store=data_store, namespace="email-approvals")

    return Pipeline(
        steps=[
            step(
                DraftComponent(),
                output_state="draft",
                input_map={"topic": "topic"},
                name="draft",
            ),
            # The datastore checkpointer makes this pause durable across processes.
            interrupt(
                name="wait_for_human",
                message="Please review",
                resume_value_map="approved",
            ),
        ],
        state_type=ApprovalState,
        checkpointer=saver,
    )


async def main() -> None:
    pipeline = build_pipeline()
    thread_id = "email-session-123"

    # 1) INVOKE — runs until it reaches the interrupt step and pauses.
    state = await pipeline.invoke(
        {"topic": "Quarterly earnings report"},
        config={"thread_id": thread_id},
    )
    print("Paused draft:", state.get("draft"))

    # 2) INSPECT — snapshot comes from the datastore, not memory.
    snapshot = await pipeline.get_state(thread_id)
    print("Next node:", snapshot.next)

    # 3) RESUME — operator approves; works even if this is a different process.
    final = await pipeline.invoke(Command(resume=True), config={"thread_id": thread_id})
    print("Approved:", final.get("approved"))

    # 4) INSPECT persisted history (newest first) and fork a what-if branch.
    history = [snap async for snap in pipeline.get_state_history(thread_id, limit=5)]
    print(f"Checkpoint history length: {len(history)}")
    for snap in history:
        cp_id = snap.config["configurable"]["checkpoint_id"]
        print("  checkpoint:", cp_id, snap.values)

    # `fork_from` (and the `delete_thread` below) exercise `get_tuple` /
    # `delete_thread` on the checkpointer. The published `DataStoreSaver`
    # (gllm-pipeline 0.5.20) implements `put`/`get`/`list` but not yet
    # `get_tuple`, so `fork_from` raises NotImplementedError upstream. We guard
    # these calls so the durable HITL flow above still runs end-to-end; uncomment
    # once a `DataStoreSaver` release implements `get_tuple`.
    oldest = history[-1].config["configurable"]
    try:
        fork_config = pipeline.fork_from(
            "email-session-whatif",
            oldest["checkpoint_id"],
            {"topic": "Q2 Marketing Performance"},
            checkpoint_ns=oldest.get("checkpoint_ns", ""),
        )
        result = await pipeline.invoke(None, config=fork_config)
        print("Forked draft:", result.get("draft"))
    except NotImplementedError:
        print(
            "fork_from: skipped — DataStoreSaver has not implemented get_tuple in "
            "the installed gllm-pipeline release; see GitBook guide section 4 for "
            "the reference API."
        )

    # 5) Delete the original thread's checkpoints once it is resolved.
    try:
        await pipeline.checkpointer.delete_thread(thread_id)
        print(f"Deleted thread '{thread_id}'s checkpoints from the datastore.")
    except NotImplementedError:
        print(
            "delete_thread: skipped — not implemented by DataStoreSaver in the "
            "installed release (GitBook guide section 5 references it)."
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
