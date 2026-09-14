"""LM Router: language-model routing.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/lm-router
"""

from __future__ import annotations

import asyncio
import os
from dotenv import load_dotenv

from gllm_inference.lm_invoker import build_lm_invoker
from gllm_inference.output_transformer import OutputTransformerConfig
from gllm_pipeline.router import LMRouter


load_dotenv()


async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipped: set OPENAI_API_KEY to run router.route().")
        return

    lm_invoker = build_lm_invoker(
        model_id="openai/gpt-5.6-luna",
        credentials=os.getenv("OPENAI_API_KEY"),
        config={"output_transformers": [OutputTransformerConfig.json()]},
    ).prompt.build(
        system_template=(
            "You are a customer support routing assistant. "
            "Analyze the customer query and pick the right department route.\n\n"
            "Available routes:\n"
            "- billing: Payment, invoices, refunds\n"
            "- tech_support: Technical issues, bugs, errors\n"
            "- sales: Product questions, pricing, features\n"
            "- general: General inquiries\n\n"
            'Respond with JSON: {"route": "<route>"}'
        ),
        user_template="Customer query: {text}",
    )

    router = LMRouter(
        lm_invoker=lm_invoker,
        default_route="general",
        valid_routes={"billing", "tech_support", "sales", "general"},
        lm_output_key="route",
    )

    for query in [
        "My credit card was charged twice for my subscription",
        "The app keeps crashing when I try to upload files",
        "What are the pricing plans for enterprise customers?",
        "How do I contact support?",
    ]:
        route = await router.route(query)
        print(f"Query: {query}\nRoute: {route}\n")

    # Only allow specific routes for this query
    # (route_filter must include default_route)
    filtered_route = await router.route(
        "My credit card was charged twice for my subscription",
        route_filter={"billing", "general"},
    )
    print(f"Filtered route: {filtered_route}")

    # Preset usage: build a router from a built-in modality preset
    preset_router = LMRouter.from_preset(
        modality="image",
        preset_kwargs={
            "default_route": "general_image",
            "valid_routes": {"general_image", "diagram"},
        },
    )
    print(f"Preset router default route: {preset_router.default_route}")


if __name__ == "__main__":
    asyncio.run(main())
