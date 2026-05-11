import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import step, transform, bundle, log


class MiniState(TypedDict):
    text: str
    text_upper: str
    text_len: int
    summary: dict


def to_upper(data: dict) -> str:
    return data["text"].upper()


def count_chars(data: dict) -> int:
    return len(data["text_upper"])


async def main() -> None:
    pipe = Pipeline(
        steps=[
            transform(to_upper, input_map=["text"], output_state="text_upper"),
            transform(count_chars, input_map=["text_upper"], output_state="text_len"),
            bundle(["text", "text_upper", "text_len"], output_state="summary"),
        ],
        state_type=MiniState,
    )

    initial: MiniState = {
        "text": "hello world",
        "text_upper": "",
        "text_len": 0,
        "summary": {},
    }
    final = await pipe.invoke(initial)
    print(final)


if __name__ == "__main__":
    asyncio.run(main())
