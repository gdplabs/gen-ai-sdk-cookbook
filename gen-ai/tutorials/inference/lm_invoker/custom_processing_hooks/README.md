## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_invoker/custom_processing_hooks
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
   ```

4. **Run the examples**

   > **Note:** Custom processing hooks are currently in beta and only available in `OpenAILMInvoker`.

   | Script | Topic |
   |---|---|
   | `uv run custom_processing_hooks_init.py` | Initialize an LM invoker with `output_hooks` and `streaming_hooks` |
   | `uv run custom_processing_hooks_output_hooks.py` | Use `output_hooks` to inspect or augment final parsed outputs |
   | `uv run custom_processing_hooks_streaming_hooks.py` | Use `streaming_hooks` to access raw streaming events |

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/custom-processing-hooks).
