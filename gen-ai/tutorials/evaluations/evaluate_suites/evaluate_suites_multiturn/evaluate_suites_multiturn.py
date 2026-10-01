"""Run a multi-turn suite end to end, and show that a suite cannot mix row types.

Covers the three ways a conversational suite is built: inline objects, a YAML file, and a CSV
whose `turns` column holds a JSON array.
"""

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
    """Build the evaluator used by every suite below.

    Returns:
        ConvEvaluator: One conversational GEval metric with a custom criterion.
    """
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
    """Build a conversation in Python.

    Returns:
        ConversationalTestCase: A booking conversation with a tool call.
    """
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
    """Convert a chat history into a conversation; the system message becomes chatbot_role.

    Returns:
        ConversationalTestCase: The converted conversation.
    """
    return ConversationalTestCase.from_messages(
        [
            Message.system("You are a cautious health information assistant."),
            Message.user("What are the side effects of ibuprofen?"),
            Message.assistant("Common side effects include stomach upset, nausea, and headache."),
        ]
    )


def conversations_from_csv() -> list[ConversationalTestCase]:
    """Load conversations whose turns are stored as a JSON array in one CSV column.

    Returns:
        list[ConversationalTestCase]: The loaded conversations.
    """
    return DictDataset.from_csv(
        str(CSV_PATH),
        test_case_type=ConversationalTestCase,
        json_columns=["turns"],
    ).load()


def show_mixed_rows_are_rejected() -> None:
    """A suite holds one row type; mixing them fails before any judge is called."""
    try:
        EvalSuite(
            data=[inline_conversation(), LLMTestCase(input="q", actual_output="a")],
            evaluators=[build_evaluator()],
        )
    except ValueError as error:
        print(f"\nmixed row types refused: {error}")


async def main():
    """Run four conversational suites together, then show the mixed-row guard."""
    suites = [
        EvalSuite(name="inline", data=[inline_conversation()], evaluators=[build_evaluator()]),
        EvalSuite(
            name="from_messages",
            data=[conversation_from_messages()],
            evaluators=[build_evaluator()],
        ),
        EvalSuite(name="from_csv", data=conversations_from_csv(), evaluators=[build_evaluator()]),
        # A YAML suite declares its own rows, evaluator and metrics, so it needs no arguments here.
        EvalSuite.from_yaml(HERE / "sample_suites" / "multiturn_inline_suite.yaml"),
    ]

    result = await evaluate_suites(suites)
    print(json.dumps({"run_id": result.run_id, "num_samples": result.num_samples}, indent=2))
    for suite_name, suite in result.suites.items():
        print(f"{suite_name}: {suite.num_samples} row(s)")

    show_mixed_rows_are_rejected()


if __name__ == "__main__":
    asyncio.run(main())
