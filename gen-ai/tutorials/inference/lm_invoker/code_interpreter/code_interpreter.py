import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as string
code_interpreter_tool = "code_interpreter"
# Option 2: as enum
code_interpreter_tool = NativeToolType.CODE_INTERPRETER
# Option 3: as dictionary (useful for providing custom kwargs)
code_interpreter_tool = {"type": "code_interpreter", **kwargs}
# Option 4: as native tool object (useful for providing custom kwargs)
code_interpreter_tool = NativeTool.code_interpreter(**kwargs)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[code_interpreter_tool])
