## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_invoker/context_management
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
   Create a file called `.env`, then set the API keys as environment variables.
   ```env
   OPENAI_API_KEY="..."
   ANTHROPIC_API_KEY="..."
   ```

4. **Run the examples**

   | Script | Topic |
   |---|---|
   | `uv run context_management_get_context_window.py` | Retrieve model context limits with `get_context_window()` |
   | `uv run context_management_count_input_tokens.py` | Estimate request size with `count_input_tokens(messages)` |
   | `uv run context_management_guarded_invocation.py` | Combine both methods to guard invocations against context overflow |

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/context-management).
