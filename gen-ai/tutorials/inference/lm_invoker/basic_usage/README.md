## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_invoker/basic_usage
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

4. **Run the example**

   ```bash
   uv run basic_usage.py
   ```

5. **Expected Output**

   You should see a response similar to the following:

   ```log
   output: Jakarta.
   ```

## 📚 Reference

This example is based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker).
