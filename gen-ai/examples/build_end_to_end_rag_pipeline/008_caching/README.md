## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/008_caching
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
   Create a file called `.env`, then set the OpenAI API key as an environment variable.

   ```env
   OPENAI_API_KEY="..."
   EMBEDDING_MODEL="text-embedding-3-small"
   LANGUAGE_MODEL="openai/gpt-5-nano"
   ```

4. **Index the dataset**

   ```bash
   uv run indexer.py
   ```

5. **Run the example**

   ```bash
   uv run pipeline.py
   ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/caching).
