# Decisions Model (DM) Invoker

These examples use the beta `OpenRouterDMInvoker` with TypeSafe decisions models. The DM invoker is intended for local prototyping; avoid using it in production environments.

## Prerequisites

See the [Gen AI SDK cookbook prerequisites](../../../README.md). Install the optional `typesafe` dependencies with the setup script and configure an OpenRouter API key.

1. Install dependencies:

   ```bash
   ./setup.sh
   ```

   On Windows, run `setup.bat` instead. Both scripts use `gcloud auth print-access-token` to authenticate to the private package index.

2. Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`.

3. Run an example:

   ```bash
   uv run 001_quickstart.py
   ```

Continue with [typed questions](./002_question_types.py), [retry and timeout](./003_retry_timeout.py), and [output analytics](./004_output_analytics.py).

Reference: [Decisions Model (DM) Invoker tutorial](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker).
