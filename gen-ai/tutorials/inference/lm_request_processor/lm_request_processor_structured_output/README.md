## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/lm_request_processor/lm_request_processor_structured_output
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
   uv run with_json_output.py
   uv run with_response_schema.py
   ```

5. **Expected Output**

   You should see a response similar to the following:

   ```log
   Structured output:
   {
      "location": "Tokyo, Japan",
      "activities": [
         {
               "type": "Sightseeing",
               "activity_location": "Tokyo Tower",
               "description": "Visit Tokyo Tower for a panoramic view of the city, especially beautiful at sunset and night."
         },
         {
               "type": "Cultural Experience",
               "activity_location": "Senso-ji Temple, Asakusa",
               "description": "Explore the historic Senso-ji Temple and the surrounding traditional shopping street, Nakamise-dori."
         },
         {
               "type": "Shopping",
               "activity_location": "Shibuya",
               "description": "Experience the famous Shibuya Crossing and shop at the trendy boutiques and department stores in the area."
         },
         {
               "type": "Food",
               "activity_location": "Tsukiji Outer Market",
               "description": "Taste fresh sushi and seafood at the famous Tsukiji Outer Market."
         },
         {
               "type": "Entertainment",
               "activity_location": "Akihabara",
               "description": "Discover the vibrant electronics and otaku culture district, with numerous shops, arcades, and themed cafes."
         }
      ]
   }
   ```

## 📚 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/utilize-language-model-request-processor/produce-consistent-output-from-lm).
