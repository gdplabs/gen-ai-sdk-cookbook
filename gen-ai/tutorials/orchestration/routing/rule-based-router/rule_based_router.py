"""Rule-Based Router — complete example.

Routes queries by keyword and pattern matching. Fully deterministic, no
external credentials required.

Based on the "Complete Example" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/rule-based-router
"""

import asyncio

from gllm_pipeline.router import RuleBasedRouter
from gllm_pipeline.router.rule_based_router import RouterRule, RouterRuleset


async def main() -> None:
    billing_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=[
                    "payment", "invoice", "billing", "charge",
                    "refund", "card", "subscription",
                ],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    tech_support_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=[
                    "crash", "error", "bug", "broken",
                    "not working", "fail", "issue",
                ],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    sales_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["pricing", "plan", "feature", "enterprise", "upgrade"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    faq_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["hours", "location", "contact", "help", "guide", "how"],
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
            "sales": sales_rules,
            "faq": faq_rules,
        },
        default_route="faq",
        valid_routes={"billing", "tech_support", "sales", "faq"},
    )

    test_cases = [
        "My credit card was charged twice",
        "The app keeps crashing on startup",
        "What are your enterprise pricing options?",
        "What are your business hours?",
        "I don't understand something",
    ]

    for query in test_cases:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")


if __name__ == "__main__":
    asyncio.run(main())
