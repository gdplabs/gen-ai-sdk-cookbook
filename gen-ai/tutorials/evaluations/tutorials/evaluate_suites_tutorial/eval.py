"""Evaluate a multi-domain customer service chatbot using evaluate_suites.

This tutorial walks through evaluating a chatbot that serves three domains,
each requiring a different evaluation strategy:

1. FAQ — general knowledge questions (generation quality)
2. Knowledge Base RAG — factuality against retrieved context (groundedness)
3. Troubleshooting — step-by-step technical guidance (generation quality)

All three domains are evaluated in a single experiment using evaluate_suites,
sharing one run_id and one tracker.

Authors:
Kalvin (kalvinsupriadi3@gmail.com)
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

# ---------------------------------------------------------------------------
# Step 2: Test Data
#
# Each domain has its own set of questions, expected answers, and — where
# applicable — retrieved context from the knowledge base.
# In production, actual_output and retrieved_context come from your deployed
# chatbot pipeline. Here we hardcode mock responses for reproducibility.
# ---------------------------------------------------------------------------

# FAQ Domain — simple factual answers, no retrieval context needed.
FAQ_TEST_CASES = [
    {
        "input": "What are your business hours?",
        "actual_output": "Our business hours are Monday to Friday, 8 AM to 9 PM.",
        "expected_output": "Monday to Friday, 8 AM to 9 PM.",
    },
    {
        "input": "Where is your office located?",
        "actual_output": "Our office is at Menara BCA, Jakarta.",
        "expected_output": "Menara BCA, Jakarta.",
    },
]

# Knowledge Base RAG Domain — answers must be grounded in retrieved context.
RAG_TEST_CASES = [
    {
        "input": "How do I reset my password?",
        "actual_output": (
            "Go to Settings > Security > Reset Password. "
            "You will receive a verification email. "
            "Click the link and enter your new password."
        ),
        "expected_output": (
            "Settings > Security > Reset Password. "
            "Verification email sent. Link expires in 24 hours."
        ),
        "retrieved_context": (
            "Password reset policy: Users can reset their password via "
            "Settings > Security. A verification email is sent to the "
            "registered email address. The reset link expires in 24 hours."
        ),
    },
    {
        "input": "What is the refund policy?",
        "actual_output": (
            "We offer full refunds within 7 days of purchase. "
            "Contact support with your order ID to initiate a refund."
        ),
        "expected_output": (
            "Full refunds within 7 days. "
            "Processed to original payment method within 5-10 business days."
        ),
        "retrieved_context": (
            "Refund policy: Full refunds are available within 7 days of purchase. "
            "Refunds are processed to the original payment method within "
            "5-10 business days."
        ),
    },
]

# Troubleshooting Domain — multi-step technical guidance, no retrieval context.
TROUBLESHOOTING_TEST_CASES = [
    {
        "input": "The app crashes when I try to upload a photo. What should I do?",
        "actual_output": (
            "First, ensure your app is updated to the latest version. "
            "Then, try clearing the app cache from Settings > Storage > "
            "Clear Cache. If the issue persists, check that the photo format "
            "is JPEG or PNG and under 25MB."
        ),
        "expected_output": (
            "Update the app. Clear app cache. "
            "Ensure image is JPEG/PNG and under 25MB."
        ),
    },
    {
        "input": "My login keeps failing even though my credentials are correct.",
        "actual_output": (
            "Check if your Caps Lock is on. Try the 'Forgot Password' flow "
            "to reset your credentials. If using SSO, ensure your organization "
            "has not revoked your access."
        ),
        "expected_output": (
            "Check Caps Lock. Use Forgot Password flow. "
            "Verify SSO access has not been revoked."
        ),
    },
]

# ---------------------------------------------------------------------------
# Step 3: Helper — Build LLMTestCase from dict
# ---------------------------------------------------------------------------

def build_case(case: dict) -> LLMTestCase:
    """Build an LLMTestCase from a test data dict.

    Args:
        case: Dict with input, actual_output, expected_output, and
            optionally retrieved_context.

    Returns:
        LLMTestCase ready for evaluation.
    """
    return LLMTestCase(
        input=case["input"],
        actual_output=case["actual_output"],
        expected_output=case["expected_output"],
        retrieved_context=case.get("retrieved_context"),
    )


# ---------------------------------------------------------------------------
# Step 4: Construct EvalSuites and Run evaluate_suites
# ---------------------------------------------------------------------------

async def main():
    judge_model = build_lm_invoker(
        model_id="openai/gpt-5-nano",
        credentials=os.getenv("OPENAI_API_KEY"),
    )

    # FAQ Suite — generation quality (completeness + redundancy)
    faq_suite = EvalSuite(
        name="faq",
        data=[build_case(c) for c in FAQ_TEST_CASES],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    # RAG Suite — answer must be grounded in the provided context
    rag_suite = EvalSuite(
        name="rag",
        data=[build_case(c) for c in RAG_TEST_CASES],
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            )
        ],
    )

    # Troubleshooting Suite — generation quality for multi-step guidance
    troubleshooting_suite = EvalSuite(
        name="troubleshooting",
        data=[build_case(c) for c in TROUBLESHOOTING_TEST_CASES],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    # All suites evaluated in one experiment
    result = await evaluate_suites(
        suites=[faq_suite, rag_suite, troubleshooting_suite],
        dataset_name="customer_service",
    )

    # -------------------------------------------------------------------
    # Step 6: Interpret the Results
    #
    #   result.suites["faq"]       → FAQ-only aggregator + per-row results
    #   result.suites["rag"]       → RAG-only aggregator + per-row results
    #   result.suites["troubleshooting"] → Troubleshooting-only
    #   result.run_aggregators_result    → Pooled (all 6 samples combined)
    # -------------------------------------------------------------------
    print("=" * 60)
    print("CUSTOMER SERVICE CHATBOT — EVALUATION RESULTS")
    print("=" * 60)
    print(f"\nRun ID: {result.run_id}")
    print(f"Total Samples: {result.num_samples}")

    for suite_name, suite_result in result.suites.items():
        agg = suite_result.run_aggregators_result
        print(f"\n  Suite '{suite_name}' ({suite_result.num_samples} samples):")
        print(f"    {json.dumps(agg, indent=4)}")

    print(f"\n  Pooled (all suites combined):")
    print(f"    {json.dumps(result.run_aggregators_result, indent=4)}")
    print(f"\n  Experiment URIs:")
    print(f"    {json.dumps(result.experiment_uris, indent=4)}")


if __name__ == "__main__":
    asyncio.run(main())
