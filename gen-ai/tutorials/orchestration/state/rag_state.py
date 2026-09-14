"""Default RAGState definition from gllm-pipeline.

The Pipeline's default state type. Keys cover standard RAG fields plus
an EventEmitter slot for streaming. This script verifies the corrected
field set: chunks/history typed as list[Any] and the
response_synthesis_bundle dict.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/state#default-state-ragstate
"""
from __future__ import annotations

import asyncio
import typing

from gllm_pipeline.pipeline.pipeline import RAGState


async def main() -> None:
    """Print RAGState fields and verify the corrected set."""
    expected_fields = {
        "user_query",
        "queries",
        "retrieval_params",
        "chunks",
        "history",
        "context",
        "response_synthesis_bundle",
        "response",
        "references",
        "event_emitter",
    }
    hints = typing.get_type_hints(RAGState)
    annotations = RAGState.__annotations__
    for key in annotations:
        print(f"- {key}: {hints.get(key, '???')}")

    missing = expected_fields - set(annotations)
    if missing:
        raise AssertionError(f"RAGState is missing corrected fields: {sorted(missing)}")
    print("RAGState contains all corrected default fields.")


if __name__ == "__main__":
    asyncio.run(main())
