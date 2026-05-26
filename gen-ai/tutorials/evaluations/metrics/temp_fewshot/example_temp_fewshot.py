import asyncio
import os

from dotenv import load_dotenv
from gllm_evals import LLMTestCase
from gllm_evals.constant import DefaultValues
from gllm_evals.metrics import GEvalCompletenessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


async def example_append_fewshot():
    """Append a fewshot example to the metric's default examples."""
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    metric = GEvalCompletenessMetric(models=model)
    data = LLMTestCase(
        input="What is the return policy for electronics?",
        actual_output="You can return electronics within 30 days with receipt.",
        expected_output="Electronics can be returned within 30 days of purchase with a valid receipt.",
    )
    result = await metric.evaluate(
        data,
        temp_fewshot=(
            "Example: Input: 'What payment methods are accepted?' "
            "Expected Output: 'We accept Visa, Mastercard, and PayPal.' "
            "Actual Output: 'We accept credit cards.' "
            "Score: 1 (the response covers the key fact about payment types but omits PayPal)"
        ),
        fewshot_mode="append",
    )
    print(f"[Append] Score: {result.score}")
    print(f"[Append] Explanation: {result.explanation}")


async def example_replace_fewshot():
    """Replace the default fewshot examples entirely."""
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    metric = GEvalCompletenessMetric(models=model)
    data = LLMTestCase(
        input="What is the return policy for electronics?",
        actual_output="You can return electronics within 30 days with receipt.",
        expected_output="Electronics can be returned within 30 days of purchase with a valid receipt.",
    )
    result = await metric.evaluate(
        data,
        temp_fewshot=(
            "Example: Input: 'How to reset password?' "
            "Actual Output: 'Go to settings, click reset password, follow the email link.' "
            "Score: 2 (the response covers all essential steps in the correct order)"
        ),
        fewshot_mode="replace",
    )
    print(f"[Replace] Score: {result.score}")
    print(f"[Replace] Explanation: {result.explanation}")


async def example_temp_info():
    """Add domain-specific context information to guide evaluation."""
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    metric = GEvalCompletenessMetric(models=model)
    data = LLMTestCase(
        input="What is the procedure for filing a medical claim?",
        actual_output="Fill out the claim form and submit it to HR.",
        expected_output="Complete the claim form, attach medical receipts, submit to HR within 90 days of treatment.",
    )
    result = await metric.evaluate(
        data,
        temp_info="Domain: Health Insurance\nAudience: New employees",
    )
    print(f"[Temp Info] Score: {result.score}")
    print(f"[Temp Info] Explanation: {result.explanation}")


async def example_combined():
    """Combine temp_fewshot and temp_info for the same evaluation."""
    model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
    metric = GEvalCompletenessMetric(models=model)
    data = LLMTestCase(
        input="Explain the company's remote work policy.",
        actual_output="Employees can work from home with manager approval.",
        expected_output="Employees may work remotely up to 3 days per week with written manager approval. "
                       "Full-time remote requires VP-level sign-off.",
    )
    result = await metric.evaluate(
        data,
        temp_fewshot=(
            "Example: Input: 'What is the vacation policy?' "
            "Actual Output: 'You get 15 days per year.' "
            "Score: 1 (missing accrual rules and carryover limits)"
        ),
        temp_info="Domain: HR Policy\nAudience: Managers reviewing team requests",
        fewshot_mode="append",
    )
    print(f"[Combined] Score: {result.score}")
    print(f"[Combined] Explanation: {result.explanation}")


async def main():
    await example_append_fewshot()
    print("---")
    await example_replace_fewshot()
    print("---")
    await example_temp_info()
    print("---")
    await example_combined()


if __name__ == "__main__":
    asyncio.run(main())
