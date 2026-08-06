from dotenv import load_dotenv
load_dotenv()

from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM

lm_invoker = AnthropicLMInvoker(AnthropicLM.CLAUDE_SONNET_4_6)
