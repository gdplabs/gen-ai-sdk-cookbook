"""Semantic Router — Aurelio backend with an explicit EMInvokerEncoder.

Uses ``SemanticRouter.aurelio()`` with a manually constructed
``EMInvokerEncoder``. Wrapping the EM invoker yourself lets you set advanced
options such as a custom encoder ``name``.

In production the wrapped invoker is a real embedding model:

    from gllm_inference.em_invoker import build_em_invoker

    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials="<YOUR_OPENAI_API_KEY>",
    )

To keep this example runnable offline, the wrapped invoker is a deterministic
``FakeEMInvoker`` (see ``fake_em.py``). The ``SemanticRouter``, the
``EMInvokerEncoder``, and the Aurelio backend are the real library code path.

Based on the "Aurelio Backend with EM Invoker Encoder" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router/aurelio-backend
"""

import asyncio

from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder

from fake_em import FakeEMInvoker


async def main() -> None:
    em_invoker = FakeEMInvoker()
    em_encoder = EMInvokerEncoder(em_invoker, name="my-encoder")

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
        encoder=em_encoder,
        route_examples=routes,
        default_route="faq",
        valid_routes=set(routes.keys()),
        similarity_threshold=0.2,
    )

    queries = [
        "My credit card expired and I can't pay my invoice",
        "The app keeps crashing when I try to upload files",
        "How do I reset my password?",
    ]

    for query in queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
