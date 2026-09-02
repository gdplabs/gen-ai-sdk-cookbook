## ⚙️ Prerequisites

Please refer to prerequisites [here](../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/observability
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

3. **Set environment variables**

   Copy `.env.example` to `.env` and set `OPENAI_API_KEY` (only `003_captured_span_attributes.py` needs it).

4. **Run the examples**

   ```bash
   uv run 001_configure_trace_content.py      # configure_lm_trace_content opt-in / disable
   uv run 002_read_config.py                  # get_lm_trace_content_config snapshot
   uv run 003_captured_span_attributes.py     # gen_ai.*.messages attributes on the LM span
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/observability).
