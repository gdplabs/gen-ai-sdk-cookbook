"""Example script to run a simple Agent and evaluate its response."""

import asyncio
import os
from dotenv import load_dotenv

from glaip_sdk.agents import Agent
from gllm_evals.evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

QUERY = "whats the capital of france ?"
EXPECTED_OUTPUT = "The capital of France is Paris."

def run_agent():
    """Runs the agent synchronously."""
    # 1. Initialize the Agent
    hello_agent = Agent(
        name="hello_local_agent",
        instruction="You are a knowledgeable assistant."
    )

    # 2. Run the Agent
    result = hello_agent.run(QUERY)
    
    response = str(result)
        
    print(f"Agent response: {response}")
    return response

async def evaluate_response(response):
    """Runs the evaluation asynchronously."""
    # 3. Evaluation
    print("\n--- Evaluation ---")
    
    test_case = LLMTestCase(
        input=QUERY,
        actual_output=response,
        expected_output=EXPECTED_OUTPUT,
    )

    judge_model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )

    evaluator = GEvalGenerationEvaluator(models=judge_model)
    
    eval_result = await evaluator.evaluate(test_case)
    
    print("Evaluation Results:")
    print(eval_result)

if __name__ == "__main__":
    agent_response = run_agent()
    
    if agent_response and not agent_response.startswith("Error:"):
        asyncio.run(evaluate_response(agent_response))
    else:
        print("\nSkipping evaluation due to agent error.")