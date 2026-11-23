import json

from gllm_inference.catalog import LMInvokerCatalog, PromptBuilderCatalog
from gllm_inference.catalog import lm_request_processor_catalog as _lmrp_catalog_mod
from gllm_inference.schema import PromptSelectionConfig

records = [
    {
        "name": "summarize",
        "system": (
            "You are an AI expert\nSummarize the following context.\n\n"
            "Context:\n```{context}```"
        ),
        "user": "",
        "kwargs": None,
    },
    {
        "name": "transform_query",
        "system": "",
        "user": (
            "Transform the following query into a simpler form.\n\n"
            "Query:\n```{query}```"
        ),
        "kwargs": None,
    },
    {
        "name": "draft_document",
        "system": (
            "You are an AI expert.\nDraft a document following the provided format "
            "and context.\n\nFormat:\n```{format}```"
        ),
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

# --- Using catalog: override default kwargs, more prompt builders (#using-catalog) ---
# Or override the default format
document_prompt = catalog.draft_document.format(
    format="Custom Format",
    context="Background information",
    query="Write a summary report",
)

# --- Loading catalog: from_csv (#loading-catalog/load-with-fromcsv-method) ---
catalog = PromptBuilderCatalog.from_csv(csv_path="sample_prompt_builder_catalog.csv")
prompt_builder = catalog.transform_query

# --- Loading catalog: from_json + from_records
# (#loading-catalog/load-with-fromjson-method) ---
# Load from JSON file
with open("sample_prompt_builder_catalog.json") as f:
    records = json.load(f)

catalog = PromptBuilderCatalog.from_records(records=records)
prompt_builder = catalog.summarize

# --- Selecting prompts from a PromptBuilderCatalog
# (#selecting-prompts-from-a-prompt-builder-catalog) ---
prompt_catalog = PromptBuilderCatalog.from_records(
    records=[
        {
            "name": "explicit_prompt",
            "system": "Answer accurately and concisely.",
            "user": "{query}",
            "kwargs": {},
        },
        {
            "name": "openai_prompt",
            "system": "You are an OpenAI model assistant.",
            "user": "{query}",
            "kwargs": {},
        },
        {
            "name": "default_prompt",
            "system": "You are a helpful assistant.",
            "user": "{query}",
            "kwargs": {},
        },
    ]
)

invoker_catalog = LMInvokerCatalog.from_records(
    records=[
        {
            "name": "router",
            "model_id": "openai/gpt-5.6",
            "credentials": "env:OPENAI_API_KEY",
            "config": {},
            "prompt_builder_name": "explicit_prompt",
        },
        {
            "name": "summarizer",
            "model_id": "openai/gpt-5-nano",
            "credentials": "env:OPENAI_API_KEY",
            "config": {},
        },
        {
            "name": "planner",
            "model_id": "openai/gpt-5.6",
            "credentials": "env:OPENAI_API_KEY",
            "config": {},
        },
        {
            "name": "analyst",
            "model_id": "anthropic/claude-sonnet-4-20250514",
            "credentials": "env:ANTHROPIC_API_KEY",
            "config": {},
        },
    ]
)

invoker_catalog.apply_prompt_selection(
    prompt_catalog,
    PromptSelectionConfig(
        model_id_prompt_names={"openai/gpt-5.6": "openai_prompt"},
        provider_prompt_names={"openai": "openai_prompt"},
        default_prompt_name="default_prompt",
    ),
)

# --- Loading catalog: LMInvokerCatalog.from_records + router attribute
# (#loading-catalog/load-using-fromrecords-method) ---
with open("sample_lm_invoker_catalog.json") as f:
    records = json.load(f)

catalog = LMInvokerCatalog.from_records(records=records)
router_invoker = catalog.router

# --- Loading catalog: LMRequestProcessorCatalog.from_json
# (#loading-catalog/load-with-fromjson-method) ---
with open("sample_lm_request_processor_catalog.json") as f:
    records = json.load(f)

catalog = _lmrp_catalog_mod.LMRequestProcessorCatalog.from_records(records=records)
