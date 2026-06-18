## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**
  ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/002_smart_image_routing
  ```
2. **Set UV authentication and install dependencies**
  Run the appropriate setup script for your system:
   **For Unix-based systems (Linux, macOS):**
   **For Windows:**
  > Alternatively, set the following env vars manually
  >
  > ```env
  > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
  > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
  > ```
  >
  > *Then run*
  >
  > ```bash
  > uv lock
  > uv sync
  > ```
3. **Prepare** `.env` **file**
  Copy `.env.example` to `.env` and fill in your credentials.
4. **Provide a PDF with embedded images**
  Place your PDF at `product_catalog.pdf` in this directory.  
   You can use the following sample file to get started:  
   [pdf-example.pdf](https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf)
5. **Index the images**
  ```bash
   uv run indexer.py
  ```
   The indexer loads the PDF, parses and chunks it into elements, then calls `LMBasedImageToCaption` directly on each image element to generate a caption. Captions are stored in ChromaDB.
6. **Run the pipeline**
  ```bash
   uv run pipeline.py
  ```
7. **Expected Output**
  ```log
  [Start 'VectorRetriever'] Processing input:                           
      - query: 'If a client does not require support with toileting, does not require support with dressing, but does require support with showering/bathing, what team  assignment and group classification do they receive?'                                                   
      - top_k: 10 
  [GoogleEMInvoker] Invoking 'google/gemini-embedding-001'
  [VectorRetriever] [Finished 'VectorRetriever'] Successfully produced output: [...]
  [Start 'ResponseSynthesizer'] Processing query: 'If a client does not require support with toileting, does not require support with dressing, but does require support with showering/bathing, what team assignment and group classification do they receive?'
  [GoogleLMInvoker] Invoking 'google/gemini-3-flash-preview'
  [Finished 'ResponseSynthesizer'] Successfully synthesized response: [...]

  Pipeline result: Based on the operational guidelines and the provided flowcharts for the **Early Supported Discharge / Rehabilitation Admission Avoidance** sub-profile (Group 4), a client with those specific needs receives the following assignment and classification:

  *   **Team Assignment:** Early Supported Discharge Team **LIGHT**
  *   **Group Classification:** **Group 4a**

  **Logic Path (from the Group 4 flowchart):**
  1.  **Require support with toileting?** No.
  2.  **Require support with dressing?** No.
  3.  **Require support with showering/bathing?** Yes. 
  4.  **Result:** This leads directly to the "Early Supported Discharge Team LIGHT" and "Group 4a" classification.

  This is further supported by the **Group 4a Client Scenario** in the text, which describes a 73-year-old male who is able to dress and toilet independently but requires assistance with showering; he is classified as Group 4a because the input required is considered "light."
  ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/image-search-pipeline).