from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_invoker.prompt.build(
    system_template="You are a helpful coding assistant.",
    user_template="Summarize this bug report in 3 bullets: {report}",
)
