"""Test cases for an online clothing store's FAQ chatbot.

Each case holds a customer question, the chatbot's answer, the expected answer, and the
policy text the chatbot retrieved.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

from gllm_evals import LLMTestCase

RETURNS_CASE = LLMTestCase(
    input="Can I return an item I bought on sale?",
    actual_output=(
        "Yes. Sale items can be returned within 14 days of delivery. "
        "You'll get store credit instead of a refund to your original payment method."
    ),
    expected_output="Yes. Sale items can be returned within 14 days of delivery, for store credit only.",
    retrieved_context=(
        "Returns: Full-price items can be returned within 30 days of delivery for a full refund. "
        "Sale items can be returned within 14 days of delivery and are refunded as store credit only. "
        "Items must be unworn and have their original tags."
    ),
)

SHIPPING_FEE_CASE = LLMTestCase(
    input="How much is shipping for an order under $50?",
    actual_output=(
        "Orders under $50 have a flat $5.99 shipping fee, and every order arrives within 2 business days. "
        "Orders of $50 or more ship free."
    ),
    expected_output="Shipping costs $5.99 for orders under $50. Orders of $50 or more ship free.",
    retrieved_context=(
        "Shipping: Standard shipping costs $5.99 for orders under $50. "
        "Orders of $50 or more qualify for free standard shipping. "
        "Standard shipping takes 3-7 business days."
    ),
)

SHIPPING_DESTINATION_CASE = LLMTestCase(
    input="Do you ship internationally?",
    actual_output="Not at the moment. We currently ship only within the United States.",
    expected_output="No. The store ships only within the United States.",
    retrieved_context=(
        "Shipping destinations: We currently ship only to addresses within the United States, "
        "including Alaska and Hawaii. We do not ship to P.O. boxes."
    ),
)
