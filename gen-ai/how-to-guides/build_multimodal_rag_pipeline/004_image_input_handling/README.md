## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/001_image_search_pipeline
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
   OPENAI_API_KEY="..."
   EMBEDDING_MODEL="text-embedding-3-small"
   LANGUAGE_MODEL="openai/gpt-4o-mini"
   DEFAULT_IMAGE_CAPTIONING_MODEL_ID="google/gemini-2.5-flash"
   GOOGLE_API_KEY="..."
   ```

4. **Provide a PDF with embedded images**  
   Place your PDF at `product_catalog.pdf` in this directory.  
   You can use the following sample file to get started:  
   [pdf-example.pdf](https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf)

   ```bash
   curl -o product_catalog.pdf https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf
   ```

5. **Index the images**

   ```bash
   uv run indexer.py
   ```

   The indexer loads the PDF, parses and chunks it into elements, then calls `LMBasedImageToCaption` directly on each image element to generate a caption. Captions are stored in ChromaDB.

   ```
   Captioned image on page 4: A three-tier wall shelf crafted from walnut with prominent natural grain...
   Captioned image on page 7: A wooden chair with light brown oak legs and a straight upright backres...
   Captioned image on page 12: A lightweight steel desk with a white laminate surface and storage dra...

   Indexed 3 images.
   ```

6. **Run the pipeline**

   ```bash
   uv run pipeline.py
   ```

7. **Expected Output**

  ```log
  [Start 'VectorRetriever'] Processing input:                           
      - query: 'Which NARP pathway and team should be assigned to this patient?\n\n[Image                 
      context: Sebuah formulir penilaian pasien untuk Group 4 Sub-Profile Assessment, merinci                 
      kebutuhan perawatan dan rencana tindakan.\nFormulir penilaian ADL (Activities of Daily                  
      Living) untuk pasien Margaret J. Davies, menunjukkan tingkat kemandiriannya dalam                       
      berbagai aktivitas.\nRincian tingkat kebutuhan dan ketergantungan perawatan, termasuk                   
      estimasi jam bantuan fisik yang diperlukan setiap hari.\nDokumen ini merupakan bagian                   
      dari proses Early Supported Discharge (ESD), mengidentifikasi dukungan yang dibutuhkan                  
      pasien sebelum pulang ke rumah.\nFormulir penilaian lengkap dengan catatan tulisan                      
      tangan yang merinci bantuan untuk berpakaian dua kali sehari dan pengawasan mandi                       
      mingguan.]'
      - top_k: 5 
  [GoogleEMInvoker] Invoking 'google/gemini-embedding-001'
  [VectorRetriever] [Finished 'VectorRetriever'] Successfully produced output: [...]
  [Start 'ResponseSynthesizer'] Processing query: 'Which NARP pathway and team should be assigned to this patient?\n\n[Image                 
      context: Sebuah formulir penilaian pasien untuk Group 4 Sub-Profile Assessment, merinci                 
      kebutuhan perawatan dan rencana tindakan.\nFormulir penilaian ADL (Activities of Daily                  
      Living) untuk pasien Margaret J. Davies, menunjukkan tingkat kemandiriannya dalam                       
      berbagai aktivitas.\nRincian tingkat kebutuhan dan ketergantungan perawatan, termasuk                   
      estimasi jam bantuan fisik yang diperlukan setiap hari.\nDokumen ini merupakan bagian                   
      dari proses Early Supported Discharge (ESD), mengidentifikasi dukungan yang dibutuhkan                  
      pasien sebelum pulang ke rumah.\nFormulir penilaian lengkap dengan catatan tulisan                      
      tangan yang merinci bantuan untuk berpakaian dua kali sehari dan pengawasan mandi                       
      mingguan.]'
  [GoogleLMInvoker] Invoking 'google/gemini-3-flash-preview'
  [Finished 'ResponseSynthesizer'] Successfully synthesized response: [...]

   Pipeline result: Based on the assessment details provided and the decision-making logic described in the flowcharts, here is the assignment for the patient, Margaret J. Davies:

   *   **NARP Pathway:** **Group 4** (Early Supported Discharge / Rehabilitation Admission Avoidance sub-profile).
   *   **Assigned Team:** **Early Supported Discharge Team MODERATE**.
  ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/search-by-image).
