"""Rule-Based Router: deterministic keyword matching router.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/rule-based-router
"""
import asyncio

from gllm_pipeline.router import RuleBasedRouter
from gllm_pipeline.router.rule_based_router import RouterRule, RouterRuleset


async def main() -> None:
    billing_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["payment", "invoice", "billing", "charge", "refund"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )
    tech_support_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["crash", "error", "bug", "broken", "not working"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    router = RuleBasedRouter(
        ruleset_map={
            "billing": billing_rules,
            "tech_support": tech_support_rules,
            "faq": RouterRuleset(
                rules=[
                    RouterRule(
                        keywords=["hours", "location", "contact", "help"],
                        allow_substring=True,
                        case_sensitive=False,
                    ),
                ],
                match_all=False,
            ),
        },
        default_route="faq",
        valid_routes={"billing", "tech_support", "faq"},
    )

    for query in [
        "My credit card was charged twice",
        "The app keeps crashing on startup",
        "What are your business hours?",
    ]:
        route = await router.route(query)
        print(f"Query: {query}\nRoute: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
