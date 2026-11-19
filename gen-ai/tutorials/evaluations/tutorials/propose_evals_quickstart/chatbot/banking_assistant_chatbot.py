"""Banking Assistant Chatbot: a bank-policy QA assistant that answers in Indonesian from a supplied policy context.

The guardrail and relevance classifiers run in order. If either rejects the question, the chatbot returns
FAILURE_RESPONSE and skips generation. All three stages use DeepSeek V4.1 Flash with the prompts in prompts/.

    import asyncio
    from banking_assistant_chatbot import BankingAssistantChatbot
    result = asyncio.run(BankingAssistantChatbot().answer({"question": "...", "context": "..."}))
    result["generated_response"]

Needs OPENROUTER_API_KEY.
"""

import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import cast

import json_repair
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.prompt_builder import PromptBuilder

FAILURE_RESPONSE = "Maaf, saya tidak bisa menjawab pertanyaan tersebut."
PROMPTS_DIR = Path(__file__).parent / "prompts"
COMPONENTS = ("guardrails", "relevant_classifier", "generation")


class BankingAssistantChatbot:
    """Run the chatbot's guardrail, relevance, and generation stages."""

    def __init__(self) -> None:
        """Load the prompts and build the model invoker."""
        self.prompts: dict[str, PromptBuilder] = {
            name: PromptBuilder(
                system_template=(PROMPTS_DIR / f"{name}.system.txt").read_text(),
                user_template=(PROMPTS_DIR / f"{name}.user.txt").read_text(),
            )
            for name in COMPONENTS
        }
        self.lm_invoker = build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={
                "provider": {"order": ["morph"], "allow_fallbacks": False},
                "default_hyperparameters": {"temperature": 0.0, "top_p": 0.001, "seed": 42},
            },
        )

    async def answer(self, data: Mapping[str, object]) -> dict[str, object]:
        """Answer one row.

        Args:
            data (Mapping[str, object]): The row, containing at least "question" and "context".

        Returns:
            dict[str, object]: The row extended with response, generated_response, predicted_is_guardrails and
                predicted_is_relevant.
        """
        result: dict[str, object] = {
            **data,
            "response": "",
            "generated_response": "",
            "predicted_is_guardrails": False,
            "predicted_is_relevant": False,
        }

        guardrail_response = await run_text_prompt(
            self.prompts["guardrails"], self.lm_invoker, query=result["question"]
        )
        result["predicted_is_guardrails"] = bool(
            self._classifier_value(guardrail_response, "guardrails", fallback=False)
        )
        if result["predicted_is_guardrails"]:
            result["generated_response"] = FAILURE_RESPONSE
            return result

        relevance_response = await run_text_prompt(
            self.prompts["relevant_classifier"], self.lm_invoker, query=result["question"], context=result["context"]
        )
        result["predicted_is_relevant"] = (
            self._classifier_value(relevance_response, "relevance", fallback="relevant") == "relevant"
        )
        if not result["predicted_is_relevant"]:
            result["generated_response"] = FAILURE_RESPONSE
            return result

        response = await run_text_prompt(
            self.prompts["generation"], self.lm_invoker, query=result["question"], context=result["context"]
        )
        result["response"] = response
        result["generated_response"] = self._extract_answer(response)
        return result

    @staticmethod
    def _classifier_value(response: str, key: str, *, fallback: object) -> object:
        """Read a classifier value, returning the fallback for malformed responses."""
        try:
            parsed: object = json_repair.loads(response.lower())
        except Exception:
            return fallback
        if isinstance(parsed, list):
            parsed = parsed[-1] if parsed else None
        if isinstance(parsed, dict):
            return cast(dict[object, object], parsed).get(key)
        return fallback

    @staticmethod
    def _extract_answer(response: str) -> str:
        """The content of the <ANSWER> tag, or the full response when no tag is present."""
        match = re.search(r"<ANSWER>\s*(.*?)\s*</ANSWER>", response, re.DOTALL | re.IGNORECASE)
        return match.group(1) if match else response


async def run_text_prompt(prompt: PromptBuilder, invoker: BaseLMInvoker, **inputs: object) -> str:
    """Format the prompt and return the model's text output.

    Empty non-query variables use the prompt's defaults or an empty string.
    """
    variables = {
        key: value if key == "query" or value else prompt.key_defaults.get(key) or "" for key, value in inputs.items()
    }
    if "context" in prompt.prompt_key_set and "context" not in variables:
        variables["context"] = prompt.key_defaults.get("context") or ""

    output = await invoker.invoke(prompt.format(**variables), max_calls=5)
    if not isinstance(output.text, str):
        raise TypeError(f"Text prompt returned {type(output.text).__name__}, expected str")
    return output.text

