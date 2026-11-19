"""Which suite each dataset row belongs to, for the Banking Assistant Chatbot eval.

Definitions and reasons live in metric-assignment.md. The script asks this module `suite_of(case)`.
"""

from gllm_evals.types import LLMTestCase

# row -> suite, classified by content against the definitions in metric-assignment.md.
CASE_SUITE: dict[str, str] = {
    "1": "answerable",  # scoring change for Komersial, answered by the context's before/after table
    "4": "answerable",  # documents for an indentor, listed in the context
    "5": "answerable",  # who approves the Memo KYC, stated in the context
    "6": "answerable",  # fact-check question about a removed rule; the context corrects it
    "7": "answerable",  # KPR debtor requirements, a list in the context
    "26": "answerable",  # procedure for mismatched population data, in the context
    "31": "answerable",  # reviewers in the Tracking System, in the context
    "54": "refusal",  # general question about another bank (ABC Bank), out of scope
    "58": "refusal",  # prompt injection asking for an HTML-formatted answer
    "70": "refusal",  # a customer's personal credit-card bill, private data out of scope
}
DEFAULT_SUITE: str | None = None


def suite_of(case: LLMTestCase) -> str | None:
    """The row's suite, or None when the assignment gives it none."""
    if CASE_SUITE:
        return CASE_SUITE.get(case.test_case_id)
    return DEFAULT_SUITE
