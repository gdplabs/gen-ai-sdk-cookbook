"""Rule-Based Router: deterministic keyword matching router.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/rule-based-router
"""
import asyncio

from gllm_pipeline.router import RuleBasedRouter
from gllm_pipeline.router.rule_based_router import (
    RouterRule,
    RouterRuleset,
    RouterSplitRule,
)


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

    # Restrict available routes at runtime (route_filter must include default_route)
    filtered_route = await router.route(
        "My credit card was charged twice", route_filter={"billing", "faq"}
    )
    print(f"Filtered route: {filtered_route}")

    # Case-sensitive matching
    case_sensitive_rule = RouterRule(
        keywords=["API", "SDK", "HTTP"],
        allow_substring=True,
        case_sensitive=True,
    )
    print(f"Case-sensitive rule keywords: {case_sensitive_rule.keywords}")

    # Input splitting: match only the first word of the query
    split_rule = RouterSplitRule(splitter=[" "], beg_index=0, end_index=1)
    command_rule = RouterRule(
        keywords=["help", "support", "info"],
        allow_substring=False,
        case_sensitive=False,
        split_rule=[split_rule],
    )
    print(f"Command rule split_rule: {command_rule.split_rule}")

    # Complex splitting patterns: chain multiple split rules
    multi_split_rule = [
        RouterSplitRule(splitter=[" "], beg_index=0, end_index=2),
        RouterSplitRule(splitter=["-"], beg_index=0, end_index=1),
    ]
    complex_rule = RouterRule(
        keywords=["error-code", "error code"],
        allow_substring=False,
        case_sensitive=False,
        split_rule=multi_split_rule,
    )
    print(f"Complex rule split_rule count: {len(complex_rule.split_rule)}")


if __name__ == "__main__":
    asyncio.run(main())
