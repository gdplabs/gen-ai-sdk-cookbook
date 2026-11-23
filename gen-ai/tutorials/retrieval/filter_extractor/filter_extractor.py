"""Example of using LMFilterExtractor to extract structured filters from natural language queries.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/filter-extractor
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.core.filters.schema import FilterOperator
from gllm_retrieval.filter_extractor.lm_filter_extractor import LMFilterExtractor
from gllm_retrieval.filter_extractor.schema import FieldDescriptor, MetadataCatalog, VectorRetrieverParams


async def main() -> None:
    load_dotenv()

    catalog = MetadataCatalog(fields=[
        FieldDescriptor(
            name="metadata.department",
            description="Owning department of the document",
            python_type=str,
            allowed_values=["InfoSec", "HR", "Finance", "Engineering"],
            allowed_operators=[FilterOperator.EQ, FilterOperator.IN],
        ),
        FieldDescriptor(
            name="metadata.content_type",
            description="Document content type",
            python_type=str,
            allowed_values=["policy", "standard", "guideline", "procedure"],
            allowed_operators=[FilterOperator.EQ, FilterOperator.IN],
        ),
    ])

    extractor = LMFilterExtractor.from_metadata_catalog(
        model_id="openai/gpt-4.1-mini",
        metadata_catalog=catalog,
        retrieval_params_type=VectorRetrieverParams,
    )

    result = await extractor.extract("top 5 InfoSec security policies")
    print(result.query)
    print(result.query_filter)
    print(result.query_options)
    print(result.retriever_params)


if __name__ == "__main__":
    asyncio.run(main())
