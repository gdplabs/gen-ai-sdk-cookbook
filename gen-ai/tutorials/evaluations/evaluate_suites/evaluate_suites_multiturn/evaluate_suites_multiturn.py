"""Run four conversational suites in one call: inline, from Messages, from CSV and from YAML."""

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from gllm_inference.schema import Message

from gllm_evals import ConversationalTestCase, LLMTestCase, ToolCall, Turn
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluate_suites import EvalSuite, evaluate_suites
from gllm_evals.evaluator.conv_evaluator import ConvEvaluator
from gllm_evals.metrics.generation.deepeval_conversational_geval import (
    DeepEvalConversationalGEvalMetric,
)

load_dotenv()

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "sample_data" / "multiturn_conversations.csv"

CRITERIA = (
    "Judge whether the assistant made real progress on the user's goal across the whole "
    "conversation, using the expected outcome as the reference for success."
)


def build_evaluator() -> ConvEvaluator:
    """Return the evaluator used by every suite built here."""
    return ConvEvaluator(
        metrics=[
            DeepEvalConversationalGEvalMetric(
                name="conversation_helpfulness",
                criteria=CRITERIA,
                threshold=0.6,
            )
        ]
    )


def inline_conversation() -> ConversationalTestCase:
    """Return a booking conversation built in Python."""
    return ConversationalTestCase(
        turns=[
            Turn(role="user", content="Book me a flight to Paris next Friday."),
            Turn(
                role="assistant",
                content="I found two options: Air France $320 and Delta $410.",
                retrieved_context=["Air France CDG 09:15 $320", "Delta CDG 14:40 $410"],
                tools_called=[
                    ToolCall(
                        name="search_flights",
                        input_parameters={"destination": "Paris", "date": "next Friday"},
                        output="Air France $320; Delta $410",
                    )
                ],
            ),
            Turn(role="user", content="Book the cheaper one."),
            Turn(role="assistant", content="Booked Air France at $320. Your reference is AF-7821."),
        ],
        chatbot_role="a helpful travel booking assistant",
        expected_output="The assistant searches, presents options, and completes the booking.",
    )


def conversation_from_messages() -> ConversationalTestCase:
    """Return a conversation converted from a chat history, whose system message becomes chatbot_role."""
    return ConversationalTestCase.from_messages(
        [
            Message.system("You are a cautious health information assistant."),
            Message.user("What are the side effects of ibuprofen?"),
            Message.assistant("Common side effects include stomach upset, nausea, and headache."),
        ]
    )


def conversations_from_csv() -> list[ConversationalTestCase]:
    """Return conversations loaded from a CSV whose turns column holds a JSON array."""
    return DictDataset.from_csv(
        str(CSV_PATH),
        test_case_type=ConversationalTestCase,
        json_columns=["turns"],
    ).load()


def show_mixed_rows_are_rejected() -> None:
    """Print the error raised when one suite mixes single-turn and multi-turn rows."""
    try:
        EvalSuite(
            data=[inline_conversation(), LLMTestCase(input="q", actual_output="a")],
            evaluators=[build_evaluator()],
        )
    except ValueError as error:
        print(f"\nmixed row types refused: {error}")


async def main():
    """Main function."""
    suites = [
        EvalSuite(name="inline", data=[inline_conversation()], evaluators=[build_evaluator()]),
        EvalSuite(
            name="from_messages",
            data=[conversation_from_messages()],
            evaluators=[build_evaluator()],
        ),
        EvalSuite(name="from_csv", data=conversations_from_csv(), evaluators=[build_evaluator()]),
        EvalSuite.from_yaml(HERE / "sample_suites" / "multiturn_inline_suite.yaml"),
    ]

    result = await evaluate_suites(suites)
    print(json.dumps({"run_id": result.run_id, "num_samples": result.num_samples}, indent=2))
    for suite_name, suite in result.suites.items():
        print(f"{suite_name}: {suite.num_samples} row(s)")

    show_mixed_rows_are_rejected()


if __name__ == "__main__":
    asyncio.run(main())
