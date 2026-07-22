"""Semantic Router: Aurelio backend using an embedding-model invoker.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#option-2-aurelio-backend-with-em-invoker
"""
from __future__ import annotations

import asyncio
import os
from dotenv import load_dotenv

from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter


load_dotenv()
async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipped: set OPENAI_API_KEY to run router.route().")
        return

    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials="<YOUR_OPENAI_API_KEY>",
    )

    routes = {
        "billing": [
            "How do I update my payment method?",
            "Invoice not received",
            "Why was I charged twice?",
        ],
        "tech_support": [
            "App crashes on launch",
            "Connection timeout when uploading",
            "Error code 504 when syncing files",
        ],
        "faq": [
            "What are your business hours?",
            "Where can I find the user guide?",
            "How do I reset my password?",
        ],
    }

    router = SemanticRouter.aurelio(
        encoder=em_invoker,
        route_examples=routes,
        default_route="faq",
        valid_routes=set(routes.keys()),
        similarity_threshold=0.5,
    )

    query = "My credit card expired and I can't pay my invoice"
    route = await router.route(query)
    print(f"Selected route: {route}")


if __name__ == "__main__":
    asyncio.run(main())
