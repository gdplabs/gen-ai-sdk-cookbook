## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/retrieval/reranker
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
   OPENROUTER_API_KEY="your-key-here"
   ```

4. **Run the example**

   ```bash
   uv run reranker.py
   uv run dm_reranker.py
   ```

   `dm_reranker.py` uses the beta decisions-model reranker with OpenRouter for local prototyping; it requires `OPENROUTER_API_KEY`. `reranker.py` requires `OPENAI_API_KEY`.

5. **Expected Output**

   ```
   1. Machine learning uses algorithms to learn from data
   2. Deep learning is a subset of machine learning
   3. Python is a programming language
   ```

   `dm_reranker.py` prints the highest-ranked chunk and its normalized relevance score (between 0 and 1); the score depends on the model's response.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/retrieval/reranker).
