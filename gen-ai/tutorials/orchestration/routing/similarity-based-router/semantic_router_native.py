"""Legacy Similarity-Based Router: deprecated in v0.5.

Migrates to SemanticRouter.native() for new code.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/similarity-based-router
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
        credentials={"api_key": "<YOUR_OPENAI_API_KEY>"},
    )

    route_examples = {
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

    router = SemanticRouter.native(
        em_invoker=em_invoker,
        route_examples=route_examples,
        default_route="faq",
        valid_routes=set(route_examples.keys()),
        similarity_threshold=0.5,
    )

    for query in [
        "My credit card was charged twice",
        "The app keeps crashing when I try to upload files",
    ]:
        route = await router.route(query)
        print(f"Query: {query}\nRoute: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
