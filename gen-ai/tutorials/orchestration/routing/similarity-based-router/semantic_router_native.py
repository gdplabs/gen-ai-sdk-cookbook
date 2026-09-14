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

    # Only allow specific routes for this query
    # (route_filter must include default_route)
    filtered_route = await router.route(
        "My credit card was charged twice", route_filter={"billing", "faq"}
    )
    print(f"Filtered route: {filtered_route}")

    # Understanding similarity_threshold: strict vs. loose vs. balanced
    for threshold in (0.8, 0.3, 0.5):
        SemanticRouter.native(
            em_invoker=em_invoker,
            route_examples=route_examples,
            default_route="faq",
            valid_routes=set(route_examples.keys()),
            similarity_threshold=threshold,
        )
    print("Constructed routers at strict/loose/balanced thresholds")

    # Using different embedding models
    em_invoker_large = build_em_invoker(
        "openai/text-embedding-3-large",
        credentials={"api_key": os.getenv("OPENAI_API_KEY")},
    )
    router_large = SemanticRouter.native(
        em_invoker=em_invoker_large,
        route_examples=route_examples,
        default_route="faq",
        valid_routes=set(route_examples.keys()),
        similarity_threshold=0.5,
    )
    print(f"Large-embedding router default route: {router_large.default_route}")

    # Dynamic route examples: add new examples by creating a new router
    updated_examples = {
        **route_examples,
        "new_route": ["Example query 1", "Example query 2"],
    }
    router_updated = SemanticRouter.native(
        em_invoker=em_invoker,
        route_examples=updated_examples,
        default_route="faq",
        valid_routes=set(updated_examples.keys()),
        similarity_threshold=0.5,
    )
    print(f"Updated router valid routes: {sorted(router_updated.valid_routes)}")


if __name__ == "__main__":
    asyncio.run(main())
