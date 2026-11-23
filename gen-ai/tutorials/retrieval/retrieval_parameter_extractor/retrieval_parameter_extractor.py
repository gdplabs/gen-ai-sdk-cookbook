"""Example of using LMBasedRetrievalParameterExtractor to infer structured retrieval parameters.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retrieval-parameter-extractor
"""

import asyncio
import json

from dotenv import load_dotenv

from gllm_inference.request_processor import build_lm_request_processor
from gllm_retrieval.retrieval_parameter_extractor.lm_based_retrieval_parameter_extractor import (
    LMBasedRetrievalParameterExtractor,
)

load_dotenv()

SYSTEM_TEMPLATE = """\
    Role: You are an assistant that extracts retrieval parameters from a user query.
    Objective: Infer a structured set of retrieval parameters that a search engine can use.

    AllowedValues (JSON):
    {{
    "department": {allowed_departments_json},
    "content_type": {allowed_content_types_json},
    "sort_fields": {allowed_sort_fields_json},
    "operators": {allowed_operators_json}
    }}

    OutputFormat (JSON):
    {{
    "query": "<string>",
    "filters": [
        {{"field": "<string>", "operator": "<operator_from_allowed_values>", "value": "<string|number|bool>"}}
    ],
    "sort": [
        {{"field": "<sort_field_from_allowed_values>", "order": "asc" | "desc"}}
    ]
    }}

    Instructions:
    - Use only values listed in AllowedValues.
    - Return ONLY a compact JSON object conforming to OutputFormat. No extra text.
"""


async def main() -> None:
    lmrp = build_lm_request_processor(
        model_id="openai/gpt-5-nano",
        system_template=SYSTEM_TEMPLATE,
        user_template="{query}",
    )

    extractor = LMBasedRetrievalParameterExtractor(lm_request_processor=lmrp)

    result = await extractor.extract_parameters(
        "Find latest InfoSec security policy documents and prioritize recent updates",
        allowed_departments_json=json.dumps(["InfoSec", "Finance", "HR", "Engineering"]),
        allowed_content_types_json=json.dumps(["security_policies", "standards", "guidelines", "procedures"]),
        allowed_sort_fields_json=json.dumps(["date", "relevance", "title"]),
        allowed_operators_json=json.dumps(["eq", "neq", "gt", "gte", "lt", "lte", "in", "nin", "like"]),
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
