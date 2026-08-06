import asyncio

router_output = asyncio.run(catalog.router.invoke("How should I answer this finance question?"))
print(router_output.text)

query_transformer_output = asyncio.run(
    catalog.query_transformer.invoke("Transform this query into search keywords: GDP trend this quarter")
)
print(query_transformer_output.text)
