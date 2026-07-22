"""Semantic Router — Native backend quickstart.

Uses ``SemanticRouter.native()``: built-in cosine-similarity routing over
per-route example sets. No training required.

In production you build a real embedding model:

    from gllm_inference.em_invoker import build_em_invoker

    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials="<YOUR_OPENAI_API_KEY>",
    )

To keep this example runnable offline, ``em_invoker`` is a deterministic
``FakeEMInvoker`` (see ``fake_em.py``). The ``SemanticRouter`` and its native
backend are the real library code path.

Based on the "Quickstart → Option 1: Native Backend" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router
"""

import asyncio

from gllm_pipeline.router import SemanticRouter

from fake_em import FakeEMInvoker


async def main() -> None:
    em_invoker = FakeEMInvoker()

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
        similarity_threshold=0.2,
    )

    query = "My credit card expired and I can't pay my invoice"
    route = await router.route(query)
    print(f"Selected route: {route}")

    # Route with filtering (route_filter must include the default_route).
    filtered = await router.route(query, route_filter={"billing", "faq"})
    print(f"Filtered route: {filtered}")


if __name__ == "__main__":
    asyncio.run(main())
