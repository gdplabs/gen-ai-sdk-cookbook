"""Default RAGState definition from gllm-pipeline.

The Pipeline's default state type. Keys cover standard RAG fields plus
an EventEmitter slot for streaming.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/state#default-state-ragstate
"""
from __future__ import annotations

import asyncio
import typing

from gllm_pipeline.pipeline.pipeline import Pipeline, RAGState
from gllm_pipeline.steps import log


async def main() -> None:
    """Print RAGState fields and run a minimal logging pipeline."""
    hints = (
        typing.get_type_hints(RAGState)
        if hasattr(RAGState, "__annotations__")
        else {}
    )
    for key in RAGState.__annotations__:
        print(f"- {key}: {hints.get(key, '???')}")

    pipeline = Pipeline(steps=[log("RAGState example", is_template=False)])
    await pipeline.invoke({})


if __name__ == "__main__":
    asyncio.run(main())
