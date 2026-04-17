import asyncio

from dotenv import load_dotenv
from gllm_inference.builder import build_lm_request_processor
from pydantic import BaseModel


load_dotenv()


class Activity(BaseModel):
    type: str
    activity_location: str
    description: str


class ActivityList(BaseModel):
    location: str
    activities: list[Activity]


lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-mini",
    system_template="You are a helpful assistant who specializes in recommending activities.",
    user_template="{question}",
    config={"response_schema": ActivityList},
)

async def main():
    response = await lmrp.process(question="I want to go to Tokyo, Japan. What should I do?")
    print(f"Structured output:\n{response.structured_output.model_dump_json(indent=4)}")  # For pretty print


if __name__ == "__main__":
    asyncio.run(main())
