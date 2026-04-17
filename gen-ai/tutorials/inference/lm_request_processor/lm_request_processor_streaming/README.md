## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/lm_request_processor/lm_request_processor_streaming
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
   uv run streaming.py
   ```

5. **Expected Output**

   You should see a response similar to the following:

   ```log
   ╭────────────────────────╮
   │     THINKING START     │
   ╰────────────────────────╯
   **Solving the Rope Puzzle**

   To solve the puzzle with two ropes, each burning for 60 minutes: light one rope at both ends and the other at one end simultaneously. The rope burning from both ends will finish in 30 minutes. Once that rope is done, light the other end of the second rope. This will take an additional 15 minutes, totaling 45 minutes. Both ropes burn unevenly, but lighting both ends halves the remaining time.
   ╭──────────────────────╮
   │     THINKING END     │
   ╰──────────────────────╯

   ╭────────────────────────╮
   │     THINKING START     │
   ╰────────────────────────╯
   **Crafting the Final Answer**

   To solve the rope puzzle, follow these steps:  
   1. Light rope A at both ends and rope B at one end simultaneously.  
   2. Rope A will burn out in 30 minutes.  
   3. Once rope A is finished, light the other end of rope B. Since rope B has been burning for 30 minutes, it has 30 minutes left to burn, but lighting it from both ends reduces this to 15 minutes. So, the total time is 45 minutes.
   ╭──────────────────────╮
   │     THINKING END     │
   ╰──────────────────────╯
   Light rope A at both ends and at the same time light rope B at one end. When rope A finishes (30 minutes), light the other end of rope B. The remaining part of B will then burn in 15 minutes, giving 30 + 15 = 45 minutes.
   ```

## 📚 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/utilize-language-model-request-processor/stream-lm-output).
