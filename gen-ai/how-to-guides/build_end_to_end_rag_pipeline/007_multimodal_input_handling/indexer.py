import os

from dotenv import load_dotenv
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.request_processor import build_lm_request_processor

load_dotenv()

response_synthesizer = ResponseSynthesizer.stuff(
    lm_request_processor=build_lm_request_processor(
        model_id=os.getenv("LANGUAGE_MODEL"),
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="""Create an imaginary animal that is similar to the animal in the picture. Context: {context}""",
        user_template="Question: {query}",
    )
)
