"""Runnable example of the full HITL lifecycle: invoke, inspect, inject, resume, fork.

Demonstrates get_state, get_state_history, update_state, fork_from, and a
structured Command(resume=...) payload in one end-to-end run.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#getstate-latest-snapshot
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#getstatehistory-full-history
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#5-updating-state-mid-run
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#6-forking-from-history
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#7-full-lifecycle-example
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#structured-resume-payloads
"""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import if_else, interrupt, step
from langgraph.checkpoint.memory import MemorySaver
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


def build_pipeline() -> Pipeline:
    """Builds the HITL pipeline used to demonstrate the full lifecycle."""
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
        checkpointer=MemorySaver(),
        name="hitl_full_lifecycle",
    )


async def email_pipeline_lifecycle() -> None:
    """Walks through invoke, inspect, inject, resume, history, and fork."""
    pipeline = build_pipeline()
    thread_id = "email-session-lifecycle"

    # 1) INVOKE - runs until the interrupt step.
    initial_state = {"topic": "Quarterly earnings report"}
    state = await pipeline.invoke(initial_state, thread_id=thread_id)
    print("Pipeline paused at wait_for_human. Draft:", state.get("email_draft"))

    # 2) INSPECT - see what the pipeline's state looks like.
    snapshot = await pipeline.get_state(thread_id)
    print("Current state values:", snapshot.values)
    print("Next nodes:", snapshot.next)

    # 3) INJECT - let the reviewer edit the draft.
    await pipeline.update_state(
        thread_id,
        {"email_draft": "REVISED: Strong performance in Q1 with record revenue."},
        as_node="wait_for_human",
    )

    # 4) RESUME - operator approves via a structured payload.
    final_result = await pipeline.invoke(
        Command(resume={"is_approved": True, "feedback": "Looks good"}),
        thread_id=thread_id,
    )
    print("Final result:", final_result.get("email_status"))

    # 5) HISTORY - review checkpoint history for audit, most-recent-first.
    print("=== History (last 3) ===")
    async for snap in pipeline.get_state_history(thread_id, limit=3):
        print(f"  {snap.config['configurable']['checkpoint_id']}: {snap.values}")

    # 6) FORK - what-if scenario from the oldest checkpoint.
    all_history = [snap async for snap in pipeline.get_state_history(thread_id)]
    first_snap = all_history[-1]
    checkpoint_id = first_snap.config["configurable"]["checkpoint_id"]
    checkpoint_ns = first_snap.config["configurable"].get("checkpoint_ns", "")

    fork_config = pipeline.fork_from(
        "email-session-whatif",
        checkpoint_id,
        {"topic": "Q2 Marketing Performance Projections"},
        checkpoint_ns=checkpoint_ns,
    )
    whatif_result = await pipeline.invoke(None, config=fork_config)
    print("What-if result:", whatif_result.get("email_status"))


async def main() -> None:
    """Runs the full HITL lifecycle demonstration."""
    await email_pipeline_lifecycle()


if __name__ == "__main__":
    asyncio.run(main())
