import os

component = MyLMComponent.from_config(
    model_id="openai/gpt-5.4-nano",
    credentials=os.environ["OPENAI_API_KEY"],
    config={"response_schema": MyResponseSchema},
    system_template="You are an expert.",
    user_template="Answer: {question}",
    prompt_builder_kwargs={"use_jinja": True},
)
