## ⚙️ Prerequisites

Please refer to prerequisites [here](../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/utilize_language_model_request_processor/002_produce_consistent_output_from_lm
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
   uv run structured_output_demo.py
   ```

4. **Expected Output**

   ```text
   Forest mascot decision
   {
     "creature": "Luminafox",
     "habitat": "moonlit forest",
     "confidence": 0.98,
     "reasoning": "The prompt asks for a forest creature with glowing fur."
   }
   Stealth sentinel decision
   {
     "creature": "Dusk Panther",
     "habitat": "twilight plains",
     "confidence": 0.93,
     "reasoning": "The prompt focuses on a stealth hunter rather than a glowing animal."
   }
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/utilize-language-model-request-processor/produce-consistent-output-from-lm).
