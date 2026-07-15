## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_request_processor
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

   | Script | Topic |
   |---|---|
   | `uv run lm_request_processor_basic_usage.py` | Quickstart: wrap a `PromptBuilder` and an `OpenAILMInvoker` into a single `LMRequestProcessor` |
   | `uv run lm_request_processor_prompt_variables.py` | Pass prompt variables into the templates at invocation time |
   | `uv run lm_request_processor_history.py` | Pass previous conversation turns via `history` |
   | `uv run lm_request_processor_extra_contents.py` | Pass extra contents (e.g. attachments) via `extra_contents` |
   | `uv run lm_request_processor_tool_calling.py` | Automatic tool execution, and inspecting raw tool calls with `auto_execute_tools=False` |
   | `uv run lm_request_processor_builder.py` | Build an LMRP in one call with `build_lm_request_processor()` |
   | `uv run lm_request_processor_components.py` | Build LM-based components with the `UsesLM` mixin, `from_lm_components`, `from_lm_request_processor`, and `fallback_lmrp` |

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-request-processor).
