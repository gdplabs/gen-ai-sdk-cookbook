## Prerequisites

Please refer to prerequisites [here](../../../README.md).

## Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/security_and_privacy/guardrail
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

3. **Prepare `.env` file (only for LM-backed examples)**

   Scripts that use `NemoGuardrailEngine` require an OpenAI API key. Copy `.env.example` to `.env` and fill in the key.

4. **Run the examples**

   ```bash
   uv run 001_input_only_moderation.py
   uv run 002_output_only_moderation.py
   uv run 003_check_both_input_and_output.py
   uv run 004_how_to_pass_input_output.py
   # uv run 005_multiple_engines.py  # requires OPENAI_API_KEY
   uv run 006_exception_propagation.py
   uv run 007_streaming_input.py
   uv run 008_streaming_output.py
   uv run 009_stream_buffer_limits.py
   uv run 010_standalone_engine.py
   ```

## Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail).
