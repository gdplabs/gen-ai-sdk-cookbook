## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_invoker/lm_invoker_web_search
   ```

2. **Set UV authentication and install dependencies**

   **For Unix-based systems (Linux, macOS):**
   ```bash
   ./setup.sh
   ```

   **For Windows:**
   ```cmd
   setup.bat
   ```

   > Alternatively, set env vars manually:
   > ```env
   > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
   > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
   > ```
   > Then run:
   > ```bash
   > uv lock
   > uv sync
   > ```

3. **Prepare `.env` file**

   Create a `.env` file (copy from `.env.example`) and fill in your values:
   ```env
   OPENAI_API_KEY="your-key-here"
   ```

4. **Run the example**

   ```bash
   uv run lm_invoker_web_search.py
   ```

5. **Expected Output**

   ```
   === Output item: 'text' ===
   Zootopia 2 grossed about $1.87 billion worldwide. Breakdown: roughly $428.1 million domestic and about $1.439 billion international. ...

   === Output item: 'citation' ===
   id='...' content='url_citation' metadata={'end_index': ..., 'start_index': ..., 'title': 'Zootopia 2 - Box Office Mojo', 'type': 'url_citation', 'url': 'https://www.boxofficemojo.com/...'} score=None
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/web-search).
