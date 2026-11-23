# Context Config

Runnable examples for the `ContextConfig` schema-agnostic context-rendering model in `gllm-core`.

`ContextConfig` centralizes four concerns that any schema (a `Chunk`, an `Attachment`, or a
custom payload) would otherwise duplicate: field selection, metadata filtering, template
validation, and JSON rendering. You declare `fields`, an optional `metadata_keys` filter, and
a `template` (composed of literal text plus portable `{context_json}`/`{metadata_json}`
placeholders and/or dynamic placeholders named after your selected fields), then call
`config.render(data)` to produce the formatted context string — or `None` when no fields are
selected. Because `ContextConfig` is generic, any schema can reuse it instead of re-implementing
validation and serialization logic.

> **Note — integration is a planned follow-up.** These examples exercise `ContextConfig` directly
> via `render()`. Wiring it into existing schemas such as `Chunk` and `Attachment` is out of scope
> for the introducing PR (gl-sdk #5673) and is tracked as separate follow-up work; do not assume an
> integrated `to_context(config)` API exists yet.

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/context_config/
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

3. **Run the examples**

   ```bash
   uv run 001_context_config_basics.py        # Construct with fields/metadata_keys/template; render with portable placeholders
   uv run 002_dynamic_field_placeholder.py     # Render using a dynamic field placeholder ({content})
   uv run 003_metadata_keys_filtering.py      # metadata_keys filtering behavior and the None return
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/context-config).
