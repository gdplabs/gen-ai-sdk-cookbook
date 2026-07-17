"""LM-Based Router: language-model routing.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/lm-based-router
"""
from __future__ import annotations

import asyncio
import os
from dotenv import load_dotenv

from gllm_inference.request_processor import build_lm_request_processor
from gllm_pipeline.router import LMBasedRouter


load_dotenv()
async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipped: set OPENAI_API_KEY to run router.route().")
        return

    lm_processor = build_lm_request_processor(
        lm_invoker_kwargs={
            "model_id": "openai/gpt-4o-mini",
            "credentials": os.getenv("OPENAI_API_KEY"),
        },
        prompt_builder_kwargs={
            "system_template": (
                "You are a customer support routing assistant. "
                "Analyze the customer query and pick the right department route.\n\n"
                "Available routes:\n"
                "- billing: Payment, invoices, refunds\n"
                "- tech_support: Technical issues, bugs, errors\n"
                "- sales: Product questions, pricing, features\n"
                "- general: General inquiries\n\n"
                "Respond with JSON: {\"route\": \"<route>\"}"
            ),
            "user_template": "Customer query: {source}",
        },
    )

    router = LMBasedRouter.native(
        lm_request_processor=lm_processor,
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


if __name__ == "__main__":
    asyncio.run(main())

