## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/deep_researcher
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
   Create a `.env` file and set the API key for the researcher you plan to use as an environment variable:

   ```env
   OPENAI_API_KEY="..."       # For OpenAIDeepResearcher
   GOOGLE_API_KEY="..."       # For GoogleDeepResearcher
   PARALLEL_API_KEY="..."     # For ParallelDeepResearcher
   PERPLEXITY_API_KEY="..."   # For PerplexityDeepResearcher
   GLODR_API_KEY="..."        # For GLOpenDeepResearcher
   ```

4. **Run the scripts**

   For a quick start, run one of the following scripts depending on which DeepResearcher subclass you want to use:

   ```bash
   uv run 01_a_deep_research_quickstart_openai.py      # Using OpenAIDeepResearcher
   uv run 01_b_deep_research_quickstart_google.py      # Using GoogleDeepResearcher
   uv run 01_c_deep_research_quickstart_perplexity.py  # Using PerplexityDeepResearcher
   uv run 01_d_deep_research_quickstart_parallel.py    # Using ParallelDeepResearcher
   uv run 01_e_deep_research_quickstart_glodr.py       # Using GLOpenDeepResearcher
   ```

   For prompt customization, run:

   ```bash
   uv run 02_deep_research_custom_prompt.py
   ```

   > Note: The prompt customization example uses OpenAIDeepResearcher, but the same approach applies to any other DeepResearcher subclass.

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/tutorials/generation/deep-researcher).
