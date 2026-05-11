## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_invoker/lm_invoker_prompt_operations
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
   uv run lm_invoker_prompt_operations.py
   ```

5. **Expected Output**

   ```
   - Transient failures (timeouts, flaky networks, temporary server hiccups) are common; retries give requests a second chance to succeed.
   - They improve reliability and user experience by reducing visible errors and increasing overall success rate without manual intervention.
   - Safe retry requires strategy: exponential backoff with jitter, a cap on attempts, respect for rate limits (e.g., 429/503), and idempotent operations to avoid duplicate effects.
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/prompt-operations).
