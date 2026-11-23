## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/generation/response_synthesizer
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
   >
   > ```env
   > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
   > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
   > ```
   >
   > _Then run_
   >
   > ```bash
   > uv lock
   > uv sync
   > ```

3. **Prepare `.env` file**
   Create a `.env` file and set the API key:

   ```env
   OPENAI_API_KEY="..."
   ```

4. **Run the scripts**

   Quickstart — stuff strategy with preset:

   ```bash
   uv run response_synthesizer.py
   ```

   Customizing the language model config:

   ```bash
   uv run custom_language_model.py
   ```

   Passing a custom LM Invoker:

   ```bash
   uv run custom_lm_invoker.py
   ```

   Using prompt variables:

   ```bash
   uv run prompt_variables.py
   ```

   Adding conversation history:

   ```bash
   uv run adding_history.py
   ```

   Adding extra contents (attachments):

   ```bash
   uv run extra_contents.py
   ```

   Customizing the extractor function:

   ```bash
   uv run custom_extractor.py
   ```

   Map Reduce strategy (preset):

   ```bash
   uv run map_reduce.py
   ```

   Refine strategy (preset):

   ```bash
   uv run refine.py
   ```

   Static List strategy (no LM required):

   ```bash
   uv run static_list.py
   ```

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer).