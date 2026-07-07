from gllm_core.schema import tool
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import ToolResult, Message
from dotenv import load_dotenv
import asyncio

load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def execute_tool_calling(lm_invoker, query, tools, prompt_builder):
    tool_dict = {t.name: t for t in tools}
    messages = prompt_builder.format(query=query)

    for _ in range(5):
        result = await lm_invoker.invoke(messages)

        if isinstance(result, str) or not result.tool_calls:
            return result if isinstance(result, str) else result.text

        assistant_content = []
        if result.text:
            assistant_content.append(result.text)
        assistant_content.extend(result.tool_calls)
        messages.append(Message.assistant(assistant_content))

        for call in result.tool_calls:
            try:
                output = await tool_dict[call.name].ainvoke(call.args)
            except Exception as e:
                output = f"Error: {e}"

            messages.append(Message.user(ToolResult(id=call.id, output=str(output))))

    return "Max iterations reached"

# Setup and execution
tools = [add, subtract, multiply]
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", tools=tools)
prompt_builder = PromptBuilder(
    system_template="You are a helpful assistant. Use tool for performing math operations. Output the final answer only.",
    user_template="Calculate: {query}"
)

query = "What is 15 + 25 then multiply by 2?"
result = asyncio.run(execute_tool_calling(lm_invoker, query, tools, prompt_builder))
print(f"Result: {result}")
