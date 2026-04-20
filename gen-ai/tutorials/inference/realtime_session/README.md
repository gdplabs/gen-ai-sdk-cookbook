## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/realtime_session
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
    Create a file called `.env`, then set the Google API key as an environment variable.
    ```env
    GOOGLE_API_KEY="..."      
    ```

4. **Tests the realtime session locally**

   For text only conversation:
   ```bash
   uv run 01_realtime_session_text_only.py
   ```

   For text + audio conversation:
   ```bash
   uv run 02_realtime_session_text_and_audio.py
   ```

   For text + audio conversation with tool calling:
   ```bash
   uv run 03_realtime_session_with_tool_calling.py
   ```

   Once the realtime session starts successfully, you can start conversing with the model!
   Try playing around by interrupting the model or asking a question about weather (In the case of the tool calling example) to see what it does!
   When you're done, simply type `/quit` to exit the conversation.

5. **Test realtime session integration with external systems**

   To integrate the realtime session to an external system, we can use the `InputEventStreamer` and `OutputEventStreamer`, where:
   1. The input events can be pushed as `RealtimeEvent` objects.
   2. The output events are streamed through the event emitter as regular `Event` objects. 
   
   Run the following example to simulate integration with an external system:
   ```bash
   uv run 04_realtime_session_integration.py
   ```


## 📚 Reference
These examples are based on the [GL SDK Gitbook documentation Tutorial page](https://gdplabs.gitbook.io/sdk/tutorials/inference/realtime-session).
