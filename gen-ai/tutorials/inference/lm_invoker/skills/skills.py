import asyncio

from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM
from gllm_inference.schema import Attachment, NativeTool


async def main() -> None:
    # Initialize the LM invoker
    lm_invoker = AnthropicLMInvoker(AnthropicLM.CLAUDE_SONNET_4_5)
    # Create a new skill
    skill_file = Attachment.from_path("path/to/skill.md")
    skill = await lm_invoker.skill.create(file=skill_file, name="My Custom Skill")

    # Immediately use the created skill in an invocation
    output = await lm_invoker.invoke(
        "Use the custom skill to process this request",
        tools=[NativeTool.skill(skill=skill)],
    )

    print(f"Output: {output.text}")


if __name__ == "__main__":
    asyncio.run(main())
