from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from pydantic import BaseModel
from typing import List
from gllm_inference.prompt_builder import PromptBuilder
import asyncio

load_dotenv()

# Define the response schema
class Activity(BaseModel):
    type: str
    activity_location: str
    description: str

class ActivityList(BaseModel):
    location: str
    activities: List[Activity]

# Define the LM invoker (no response schema)
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini", output_transformer="json")

# Define the prompt with schema instruction
system_template = "You are a helpful assistant who specializes in recommending activities. Return the response in JSON format with the schema: {schema}."
user_template = "{question}"

prompt_builder = PromptBuilder(system_template=system_template, user_template=user_template)

# Define the LM request processor
lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)

# Invoke the LM request processor with schema parameter
response = asyncio.run(lm_request_processor.process(
    question="I want to go to Tokyo, Japan. What should I do?",
    schema=str(ActivityList.model_json_schema())
))

print(response.structured_output)
