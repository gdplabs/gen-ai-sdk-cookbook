import asyncio

from dotenv import load_dotenv

from gllm_inference.input_transformer import InputTransformerConfig
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

load_dotenv()


async def main() -> None:
    # Configure multiple input transformers in accepted formats
    input_transformers = [
        # Option 1: as string
        "identity",
        # Option 2: as dictionary
        {"type": "filter_empty"},
        # Option 3: as config object
        InputTransformerConfig.filter_empty(),
    ]

    lm_invoker = OpenAILMInvoker(
        OpenAILM.GPT_5_NANO,
        input_transformers=input_transformers,
    )

    # filter_empty will strip out empty/whitespace-only strings before sending to the model
    output = await lm_invoker.invoke(["Name a country in Southeast Asia!", " ", ""])
    print(output.text)


if __name__ == "__main__":
    asyncio.run(main())
