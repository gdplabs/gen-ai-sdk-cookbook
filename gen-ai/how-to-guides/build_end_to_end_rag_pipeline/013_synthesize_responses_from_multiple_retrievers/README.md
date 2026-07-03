## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/013_synthesize_responses_from_multiple_retrievers
   ```

2. **Set UV authentication and install dependencies**  
   Run the appropriate setup script for your system:

   **For Unix-based systems (Linux, macOS):**
   ```bash
   ./setup.sh
   ```

   **For Windows:**
   ```cmd
   setup.bat
   ```

   > Alternatively, set the following env vars manually
   > ```env
   > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
   > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
   > ```
   >
   > *Then run*
   > ```bash
   > uv lock
   > uv sync
   > ```

3. **Prepare `.env` file**  
    Create a file called `.env`, then set the following environment variables.
    Use the same embedding model for indexing and vector retrieval. Smart Search
    credentials are only needed for the external (web) retriever branch — see the
    [Authentication guide](https://gdplabs.gitbook.io/sdk/gl-smart-search/guides/authentication)
    to get a token.
    ```env
    OPENAI_API_KEY="..."
    EMBEDDING_MODEL="text-embedding-3-small"
    LANGUAGE_MODEL="openai/gpt-5-nano"

    SMART_SEARCH_BASE_URL="<YOUR_SMART_SEARCH_BASE_URL>"
    SMART_SEARCH_TOKEN="<YOUR_SMART_SEARCH_TOKEN>"
    ```

4. **Run the example**

   ```bash
   uv run pipeline.py
   ```

   This ingests sample internal chunks into Chroma (so the example is runnable
   from a clean project — in production, run ingestion separately, see
   [index-your-data-with-vector-data-store.md](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/index-your-data-with-vector-data-store)),
   retrieves from both the internal `VectorRetriever` and the external
   `SmartSearchWebRetriever` in parallel, deduplicates and trims the merged
   chunks, then synthesizes a final response.

## Troubleshooting

- **The web branch returns no chunks**: verify `SMART_SEARCH_BASE_URL` and
  `SMART_SEARCH_TOKEN` are set (see the
  [Authentication guide](https://gdplabs.gitbook.io/sdk/gl-smart-search/guides/authentication)
  to get a token), then test the web retriever independently before running
  the full pipeline.
- **The vector branch returns irrelevant chunks**: the query embedding model
  must match the model used during indexing.
- **Duplicate chunks appear in the final context**: keep `DedupeChunkProcessor`
  in the pipeline and ensure chunks have stable IDs.

## 🚀 Reference
This example is based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/synthesize-responses-from-multiple-retrievers).
