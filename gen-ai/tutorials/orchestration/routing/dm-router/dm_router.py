"""DM Router: decisions-model routing.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/dm-router
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from gllm_inference.dm_invoker import build_dm_invoker
from gllm_pipeline.router import DMRouter

load_dotenv()


async def main() -> None:
    """Route a customer query with a decisions model."""
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Skipped: set OPENROUTER_API_KEY to run router.route().")
        return

    dm_invoker = build_dm_invoker(
        model_id="openrouter/typesafe/jev-1.13",
        credentials=os.getenv("OPENROUTER_API_KEY"),
    )

    router = DMRouter(
        dm_invoker=dm_invoker,
        route_criteria={
            "billing": "Payments, invoices, refunds",
            "tech_support": "Bugs, errors, technical issues",
            "sales": "Pricing and product questions",
            "general": None,
        },
        default_route="general",
    )

    route = await router.route("My credit card was charged twice")
    print(f"Selected route: {route}")

    route = await router.route(
        "My credit card was charged twice",
        route_filter={"billing", "general"},
    )
    print(f"Selected route (filtered): {route}")


if __name__ == "__main__":
    asyncio.run(main())
