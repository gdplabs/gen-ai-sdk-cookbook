## ⚙️ Prerequisites

Please refer to prerequisites [here](../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/utilize_language_model_request_processor/003_stream_lm_output
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

3. **Run the example**

   ```bash
   uv run stream_output_demo.py
   ```

4. **Expected Output**

   ```text
   Captured events
   1. status: Starting response stream
   2. response: Luminafox
   3. response: glows
   4. response: through
   5. response: the
   6. response: forest.
   7. status: Stream completed
   Final text
   Luminafox glows through the forest.
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/utilize-language-model-request-processor/stream-lm-output).
