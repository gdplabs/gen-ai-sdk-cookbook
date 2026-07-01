import asyncio
from gllm_pipeline.router import RuleBasedRouter
from gllm_pipeline.router.rule_based_router import RouterRule, RouterRuleset

# Define rules for each route
billing_rules = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["payment", "invoice", "billing", "charge", "refund"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=False,  # Match any rule
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

faq_rules = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["hours", "location", "contact", "help", "guide"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=False,
)

# Map routes to rulesets
ruleset_map = {
    "billing": billing_rules,
    "tech_support": tech_support_rules,
    "faq": faq_rules,
}
