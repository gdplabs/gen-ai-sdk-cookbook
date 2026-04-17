import asyncio

from dotenv import load_dotenv
from gllm_core.event import EventEmitter
from gllm_inference.builder import build_lm_request_processor


load_dotenv()


lmrp = build_lm_request_processor(
    model_id="openai/gpt-5-mini",
    system_template="You are a helpful assistant. Help the user to answer the riddle.",
    user_template="{riddle}",
    config={"reasoning_summary": "detailed"},
)
event_emitter = EventEmitter.with_print_handler()


async def main():
    await lmrp.process(
        riddle=(
            "You have two ropes and a lighter. "
            "Each rope takes exactly one hour to burn but doesn't burn evenly. "
            "How do you measure 45 minutes?",
        ),
        event_emitter=event_emitter,
    ) 


if __name__ == "__main__":
    asyncio.run(main())
