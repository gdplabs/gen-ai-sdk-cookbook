"""LM-Based Router — complete example.

The LM-Based Router asks a language model to pick a route. In production you
build the LM request processor with your credentials, exactly as shown in the
GitBook page:

    from gllm_inference.request_processor import build_lm_request_processor

    lm_processor = build_lm_request_processor(
        lm_invoker_kwargs={
            "model_id": "openai/gpt-5-nano",
            "credentials": "<YOUR_OPENAI_API_KEY>",
        },
        prompt_builder_kwargs={
            "system_template": "You are a customer support routing assistant...",
            "user_template": "Customer query: {source}",
        },
    )
    router = LMBasedRouter.native(
        lm_request_processor=lm_processor,
        default_route="general",
        valid_routes={"billing", "tech_support", "sales", "general"},
        lm_output_key="route",
    )

To keep this example runnable offline (no API key, no network), the live LM
call is stubbed with ``StubLMRequestProcessor`` below. Everything else — the
``LMBasedRouter``, route extraction, validation, and ``route_filter`` — is the
real library code path.

Based on the "Complete Example" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/lm-based-router
"""

import asyncio
from typing import Any

from gllm_pipeline.router import LMBasedRouter

# Keyword hints that a real LM would infer from the query semantics.
_ROUTE_HINTS = {
    "billing": ("charge", "invoice", "payment", "subscription", "refund"),
    "tech_support": ("crash", "error", "bug", "upload", "slow"),
    "sales": ("pricing", "plan", "enterprise", "feature", "upgrade"),
}


class StubLMRequestProcessor:
    """Stand-in for a real LM request processor (offline, deterministic)."""

    async def process(self, text: str, **_: Any) -> dict[str, str]:
        lowered = text.lower()
        for route, hints in _ROUTE_HINTS.items():
            if any(hint in lowered for hint in hints):
                return {"route": route}
        return {"route": "general"}


async def main() -> None:
    router = LMBasedRouter.native(
        lm_request_processor=StubLMRequestProcessor(),
        default_route="general",
        valid_routes={"billing", "tech_support", "sales", "general"},
        lm_output_key="route",
    )

    queries = [
        "My credit card was charged twice for my subscription",
        "The app keeps crashing when I try to upload files",
        "What are the pricing plans for enterprise customers?",
        "How do I contact support?",
    ]

    for query in queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
