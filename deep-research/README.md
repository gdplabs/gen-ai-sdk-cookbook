## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/deep-research
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
   Create a file called `.env`, then set the OpenAI API key as an environment variable.

   ```env
   OPENAI_API_KEY="..."
   ```

4. **Run the scripts**

   For simple deep research pipeline:

   ```bash
   uv run 01_deep_research_pipeline.py
   ```

   For deep research pipeline with Google Drive integration:
   Add the following environment variables to the `.env` file:

   ```env
   GOOGLE_DRIVE_AUTH_TOKEN="..."
   ```

   Get the token from: https://platform.openai.com/docs/guides/tools-connectors-mcp?quickstart-panels=connector#authorizing-a-connector

   **Important:** When generating the Google OAuth token, make sure to enable the following scopes:
   - `userinfo.email`
   - `userinfo.profile`
   - `drive.readonly`

   Then run the script:

   ```bash
   uv run 02_deep_research_google_drive_pipeline.py
   ```

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/tutorials/generation/deep-researcher).
