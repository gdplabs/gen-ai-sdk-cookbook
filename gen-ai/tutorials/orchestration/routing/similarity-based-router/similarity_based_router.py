"""Similarity-Based Router — complete example.

Measures embedding similarity between the input and per-route example sets.

Note: ``SimilarityBasedRouter`` is deprecated in v0.5 and superseded by
``SemanticRouter.native()`` — which is what the GitBook page and this example
use.

In production you build a real embedding model:

    from gllm_inference.em_invoker import build_em_invoker

    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials={"api_key": "<YOUR_OPENAI_API_KEY>"},
    )

To keep this example runnable offline, ``em_invoker`` is a deterministic
``FakeEMInvoker`` (see ``fake_em.py``). The ``SemanticRouter`` and its
similarity backend are the real library code path.

Based on the "Complete Example" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/similarity-based-router
"""

import asyncio

from gllm_pipeline.router import SemanticRouter

from fake_em import FakeEMInvoker


async def main() -> None:
    em_invoker = FakeEMInvoker()

    route_examples = {
        "billing": [
            "How do I update my payment method?",
            "Invoice not received",
            "Why was I charged twice?",
            "Can I get a refund?",
            "How do I cancel my subscription?",
            "What is my current balance?",
            "When is my payment due?",
        ],
        "tech_support": [
            "App crashes on launch",
            "Connection timeout when uploading",
            "Error code 504 when syncing files",
            "The app is very slow",
            "I can't log in to my account",
            "The app won't open",
            "I'm getting an error message",
        ],
        "sales": [
            "What are your pricing plans?",
            "Do you offer enterprise pricing?",
            "What features are included in the pro plan?",
            "Can I upgrade my plan?",
            "Do you offer discounts for annual billing?",
        ],
        "faq": [
            "What are your business hours?",
            "Where can I find the user guide?",
            "How do I reset my password?",
            "What payment methods do you accept?",
            "How do I contact support?",
        ],
    }

    router = SemanticRouter.native(
        em_invoker=em_invoker,
        route_examples=route_examples,
        default_route="faq",
        valid_routes=set(route_examples.keys()),
        similarity_threshold=0.2,
    )

    test_queries = [
        "My credit card was charged twice",
        "The app keeps crashing when I try to upload files",
        "What are your enterprise pricing options?",
        "What time do you close on weekends?",
        "I forgot my password",
    ]

    print("Routing Results:")
    print("-" * 50)

    for query in test_queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
