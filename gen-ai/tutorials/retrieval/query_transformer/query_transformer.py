from pydantic import BaseModel


class TransformResult(BaseModel):
    query: str | list[str]


SYSTEM_TEMPLATE = """
You are a helpful assistant that rewrites queries for better retrieval.
Rewrite the following query. Only output the transformed query as JSON with the following format:
{{"query": "<your-result>"}}
"""

lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-nano",
    config={"response_schema": TransformResult},
    system_template=SYSTEM_TEMPLATE,
    user_template="{query}",
)

transformer = OneToOneQueryTransformer(
    lm_request_processor=lmrp,
    extract_func=lambda lm_output: lm_output.structured_output.query  # The output is an LMOutput object. Access the Pydantic model in the `structured_output` attribute.
)

result = asyncio.run(transformer.transform("Rewrite for better retrieval: diffusion transformers"))
print(result[0])  # ['rewritten text']
