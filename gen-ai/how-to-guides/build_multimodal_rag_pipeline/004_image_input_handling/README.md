## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/004_image_input_handling
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
      - query: 'Which NARP pathway and team should be assigned to this patient?'
         [Image context: Formulir penilaian sub-profil untuk pemulangan dini (Early Supported Discharge - ESD) pasien, menampilkan informasi penting mengenai kebutuhan perawatan.\nDetail pasien Margaret J. Davies dengan tanggal lahir 14 Mei 1951, dan tanggal penilaian pada 22 November 2024.\nSkor ADL (Activities of Daily Living) menunjukkan kebutuhan bantuan signifikan untuk berpakaian (5/10) dan pengawasan untuk mandi/shower (5/10).\nTingkat kebutuhan perawatan dan ketergantungan pasien, termasuk perkiraan 2-3 jam bantuan fisik harian dan pengawasan mandi mingguan.\nRencana tindakan penilaian mencakup rujukan ke tim ESD, bantuan di rumah untuk berpakaian dan pengawasan mandi, serta tinjauan mobilitas berkelanjutan.]
      - top_k: 5
   [Finished 'VectorRetriever'] Successfully produced output: [...]

   [Start 'ResponseSynthesizer'] Processing query: '...'
   [Finished 'ResponseSynthesizer'] Successfully synthesized response: [...]

   Pipeline result: The flowchart you submitted matches the NARP Group 4 classification
   decision tree. It covers Early Supported Discharge eligibility and branches on three
   personal care criteria: toileting, dressing, and showering/bathing support requirements,
   leading to Group 4a (light support) or Group 4b (moderate support) assignments.
   ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/image-input-handling).
