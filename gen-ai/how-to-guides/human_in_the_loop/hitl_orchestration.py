"""Runnable example for human-in-the-loop orchestration."""

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
        name="hitl_demo",
    )


async def run_session(topic: str, thread_id: str, decision: bool) -> None:
    pipeline = build_pipeline()
    config = {"thread_id": thread_id}

    paused_state = await pipeline.invoke({"topic": topic}, config=config)
    print(f"Paused draft for {thread_id}: {paused_state['email_draft']}")

    final_state = await pipeline.invoke(Command(resume=decision), config=config)
    print(f"Decision for {thread_id}: {decision}")
    print(f"Final status for {thread_id}: {final_state['email_status']}")


async def main() -> None:
    await run_session("Quarterly earnings report", "email-session-approve", True)
    await run_session("Internal incident summary", "email-session-reject", False)


if __name__ == "__main__":
    asyncio.run(main())
