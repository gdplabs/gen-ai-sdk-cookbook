"""Semantic Router: load a predefined customer-support preset.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#using-presets
"""
from __future__ import annotations

import asyncio

from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.schema import BackendType, ModalityType


async def main() -> None:
    router = SemanticRouter.from_preset(
        backend=BackendType.AURELIO,
        preset_name="customer_support",
        modality=ModalityType.TEXT,
        default_route="general",
        valid_routes={"billing", "tech_support", "general"},
    )

    for query in [
        "I was charged twice for my plan",
        "The app crashes when the screen rotates",
        "Where is your European office located?",
    ]:
        route = await router.route(query)
        print(f"Query: {query}\nRoute: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
