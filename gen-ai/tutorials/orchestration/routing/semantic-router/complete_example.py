"""Semantic Router — complete example (native backend).

End-to-end routing over billing / tech_support / faq using the native backend.

In production you build a real embedding model:

    from gllm_inference.em_invoker import build_em_invoker

    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials="<YOUR_OPENAI_API_KEY>",
    )

To keep this example runnable offline, ``em_invoker`` is a deterministic
``FakeEMInvoker`` (see ``fake_em.py``).

Based on the "Complete Example" section of the GitBook page:
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

    queries = [
        "My credit card expired and I can't pay my invoice",
        "The app keeps crashing when I try to upload files",
        "What time do you close on weekends?",
    ]

    for query in queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
