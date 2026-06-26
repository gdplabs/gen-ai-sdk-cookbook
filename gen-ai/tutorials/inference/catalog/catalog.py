from gllm_inference.catalog.prompt_builder_catalog import PromptBuilderCatalog

# Method 1: Using client email and private key
catalog = PromptBuilderCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    client_email="your_service_account_email",
    private_key="your_private_key",
)

# Method 2: Using credential file
catalog = PromptBuilderCatalog.from_gsheets(
    sheet_id="your_sheet_id",
    worksheet_id="0",
    credential_file_path="path/to/credentials.json" #contains client_email and private_key
)
