"""Semantic Router: load a preset but choose the encoder via ``model_id``.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#choosing-the-preset-encoder
"""
from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.schema import BackendType, ModalityType

load_dotenv()

async def main() -> None:
    """Build a preset router whose encoder is a GLLM EM Invoker."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipped: set OPENAI_API_KEY to run router.route().")
        return

    # ``model_id`` builds an EM Invoker internally (via build_em_invoker) and uses it as
    # the preset encoder instead of the backend default. ``credentials`` and ``config``
    # are forwarded to it; ``model_id`` and an explicit ``encoder`` cannot both be set.
    # For an image preset, pass modality=ModalityType.IMAGE and a multimodal embedding
    # such as "twelvelabs/Marengo-3.0" (needs the matching gllm-inference extra).
    router = SemanticRouter.from_preset(
        backend=BackendType.AURELIO,
        preset_name="customer_support",
        modality=ModalityType.TEXT,
        model_id="openai/text-embedding-3-small",
        credentials=os.environ["OPENAI_API_KEY"],
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
