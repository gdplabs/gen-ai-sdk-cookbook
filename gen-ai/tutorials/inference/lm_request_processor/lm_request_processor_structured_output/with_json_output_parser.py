import asyncio
import json

from dotenv import load_dotenv
from gllm_inference.builder import build_lm_request_processor
from pydantic import BaseModel


load_dotenv()


SYSTEM_TEMPLATE = """You are a helpful assistant who specializes in recommending activities. 
Return the response in JSON format with the schema: {schema}."""
USER_TEMPLATE = "{question}"


class Activity(BaseModel):
    type: str
    activity_location: str
    description: str


class ActivityList(BaseModel):
    location: str
    activities: list[Activity]


lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-mini",
    system_template=SYSTEM_TEMPLATE,
    user_template=USER_TEMPLATE,
    output_parser_type="json",
)


async def main():
    schema = str(ActivityList.model_json_schema())
    response = await lmrp.process(question="I want to go to Tokyo, Japan. What should I do?", schema=schema) 
    print(f"Structured output:\n{json.dumps(response, indent=4)}")  # For pretty print


if __name__ == "__main__":
    asyncio.run(main())
