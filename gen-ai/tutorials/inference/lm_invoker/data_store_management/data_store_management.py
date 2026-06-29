from dotenv import load_dotenv
load_dotenv()

from gllm_inference.lm_invoker import GoogleLMInvoker

lm_invoker = GoogleLMInvoker("gemini-3.1-flash-lite-preview")
