"""Semantic Router: native backend for embedding-based routing.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router
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

    router = SemanticRouter.native(
        em_invoker=em_invoker,
        route_examples=routes,
        default_route="faq",
        valid_routes=set(routes.keys()),
        similarity_threshold=0.5,
    )

    for query in [
        "My credit card expired and I can't pay my invoice",
        "The app keeps crashing when I try to upload files",
        "What time do you close on weekends?",
    ]:
        route = await router.route(query)
        print(f"Query: {query}\nRoute: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
