## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/004_video_search_pipeline
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
   Copy `.env.example` to `.env` and fill in your credentials.
   ```env
   EMBEDDING_MODEL="text-embedding-3-small"
   LANGUAGE_MODEL="openai/gpt-4o-mini"
   DEFAULT_TRANSCRIBER_MODEL_ID="google/gemini-2.5-flash"
   OPENAI_API_KEY="..."
   GOOGLE_API_KEY="..."
   ```

   > `DEFAULT_TRANSCRIBER_MODEL_ID` controls which model `HybridVideoToCaption.from_preset("e2e_audio_driven")` uses.  
   > With `google/gemini-2.5-flash`, the preset builds a `GeminiAudioToText` transcriber automatically.

4. **Index the video**

   ```bash
   uv run indexer.py
   ```

   The indexer sends the YouTube URL to `HybridVideoToCaption` using the `e2e_audio_driven` preset. `GeminiAudioToText` transcribes the audio end-to-end and the result is segmented into timestamped chunks. One chunk is created for the overall video summary and one per segment.

   ```
   Processed 'Product Demo': 4 segments
     Summary: The video opens with an overview of the product lineup, followed by a
     detailed walkthrough of key features and a live demonstration...

   Indexed 5 chunks.
   ```

5. **Run the pipeline**

   ```bash
   uv run pipeline.py
   ```

6. **Expected output**

   ```
   Pipeline result: The setup guide appears in two sections of the demo video:

   - **02:15** — Step-by-step setup instructions, including component placement and initial configuration.
   - **03:40** — Final adjustment walkthrough, showing calibration and verification steps.

   You can skip directly to those timestamps in the video for the visual walkthrough.
   ```

   Users get direct timestamp references instead of just a text answer, reducing the time spent scrubbing through videos.

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/video-search-pipeline).
