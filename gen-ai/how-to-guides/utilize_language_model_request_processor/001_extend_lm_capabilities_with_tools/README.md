## ⚙️ Prerequisites

Please refer to prerequisites [here](../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/utilize_language_model_request_processor/001_extend_lm_capabilities_with_tools
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
   uv run tools_demo.py
   ```

4. **Expected Output**

   ```text
   Initial tool request
   Assistant text: I need fresh creature data before I answer.
   Tool call: creature_profile({'name': 'Luminafox'})
   Auto-executed answer
   Final answer: Luminafox is the glowing creature. Tool evidence: Luminafox glows in the dark because its silver fur reflects ambient moonlight.
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/utilize-language-model-request-processor/extend-lm-capabilities-with-tools).
