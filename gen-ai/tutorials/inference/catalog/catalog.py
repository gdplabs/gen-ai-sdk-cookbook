from gllm_inference.catalog.prompt_builder_catalog import PromptBuilderCatalog

records = [
    {
        "name": "summarize",
        "system": "You are an AI expert\nSummarize the following context.\n\nContext:\n```{context}```",
        "user": "",
        "kwargs": None,
    },
    {
        "name": "transform_query",
        "system": "",
        "user": "Transform the following query into a simpler form.\n\nQuery:\n```{query}```",
        "kwargs": None,
    },
    {
        "name": "draft_document",
        "system": "You are an AI expert.\nDraft a document following the provided format and context.\n\nFormat:\n```{format}```",
        "user": "User instruction:\n{query}",
        "kwargs": {
            "key_defaults": {
                "format": "I. Background\nII. Content\nIII. Conclusion"
            }
        },
    },
]

catalog = PromptBuilderCatalog.from_records(records=records)

summary_prompt = catalog.summarize.format(context="Some text to summarize")
print("=== Summarize Prompt ===")
print(summary_prompt)

query_prompt = catalog.transform_query.format(query="Complex query here")
print("\n=== Transform Query Prompt ===")
print(query_prompt)

document_prompt = catalog.draft_document.format(
    context="Background information",
    query="Write a summary report",
)
print("\n=== Draft Document Prompt (default format) ===")
print(document_prompt)
