from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import if_else, interrupt, step


class PipelineState(TypedDict, total=False):
    topic: str
    email_draft: str
    hitl_decision: bool
    email_status: str


# Simple executable components
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


draft_email = step(GenerateDraftComponent(), output_state="email_draft", input_map={"topic": "topic"}, name="draft_email")
send_email = step(SendEmailComponent(), output_state="email_status", input_map={"body": "email_draft"}, name="send_email")
discard_draft = step(DiscardDraftComponent(), output_state="email_status", name="discard_draft")

# Branching based on human decision
conditional_send = if_else(
    condition=lambda state: state.get("hitl_decision", False),
    if_branch=send_email,
    else_branch=discard_draft,
    name="handle_decision",
)

memory = MemorySaver()

pipeline = Pipeline(
    steps=[
        draft_email,
        # Pauses execution and asks for human intervention
        interrupt(
            name="wait_for_human",
            message={"alert": "Please review the email draft", "priority": "high"},
            resume_value_map="hitl_decision",
        ),
        conditional_send,
    ],
    state_type=PipelineState,
    checkpointer=memory,
)
