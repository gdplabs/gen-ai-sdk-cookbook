"""Input and Output Schema with TypedDict for simple filtering.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-typeddict-for-simple-schemas
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class TextProcessingState(TypedDict):
    raw_text: str
    processed_text: str
    char_count: int


class TextInput(TypedDict):
    raw_text: str


class TextOutput(TypedDict):
    processed_text: str
    char_count: int


def process_text(data: dict) -> str:
    return data["raw_text"].upper()


def count_chars(data: dict) -> int:
    return len(data["processed_text"])


def main() -> None:
    """Pipeline with input_type and output_type for schema filtering."""
    pipe = Pipeline(
        steps=[
            transform(
                process_text, input_map=["raw_text"], output_state="processed_text"
            ),
            transform(
                count_chars, input_map=["processed_text"], output_state="char_count"
            ),
        ],
        state_type=TextProcessingState,
        input_type=TextInput,   # Only 'raw_text' is required as input
        output_type=TextOutput,  # Only these fields will be in the output
    )

    initial_state = {
        "raw_text": "hello world",
        "processed_text": "",  # Still need to initialize state fields
        "char_count": 0,
    }
    result = asyncio.run(pipe.invoke(initial_state))
    print(result)  # Only contains 'processed_text' and 'char_count' (output schema)


if __name__ == "__main__":
    main()
