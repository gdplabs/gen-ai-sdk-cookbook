## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/005_simple_video_rag_pipeline
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

   ```
   EMBEDDING_MODEL="voyage-multimodal-3"
   LANGUAGE_MODEL="google/gemini-3-flash-preview"
   DEFAULT_IMAGE_CAPTIONING_MODEL_ID="google/gemini-2.5-flash"
   GOOGLE_API_KEY="..."
   VOYAGE_API_KEY="..."
   ```

4. **Index the images**

   ```bash
   uv run indexer.py
   ```

5. **Run the pipeline**

   ```bash
   uv run pipeline.py
   ```

6. **Expected Output**

   ```log
   [Start 'VectorRetriever'] Processing input:
      - query: 'What is the attention mechanism?'
      - top_k: 10
   [Finished 'VectorRetriever'] Successfully produced output: [...]

   [Start 'ResponseSynthesizer'] Processing query: 'What is the attention mechanism?'
   [Finished 'ResponseSynthesizer'] Successfully synthesized response: [...]

   Pipeline result: The attention mechanism, specifically the **self-attention mechanism** introduced in the "Attention Is All You Need" paper, is a method that allows a model to understand context by looking at an entire sentence at once rather than processing words one by one.

   Key aspects of the mechanism include:
   *   **Contextual Understanding:** At its core, it is about context. It enables the model to determine how each word in a sentence relates to every other word (02:48).
   *   **Parallel Processing:** Unlike previous models that processed data sequentially, the self-attention mechanism allows the model to look at the whole picture simultaneously to identify which parts of the input are most relevant to the current task (04:11).
   *   **Weighting Relevance:** It essentially assigns different levels of "importance" or "attention" to various words in a sequence to better understand the meaning of the text (Summary).
   ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/simple-video-rag-pipeline).
