## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/001_simple_image_rag_pipeline
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
      - query: 'Deskripsikan seperti apa bentuk rumah Suku Bajo di atas air dan tata letak desa panggung mereka?'
      - top_k: 5
   [Finished 'VectorRetriever'] Successfully produced output: [...]

   [Start 'ResponseSynthesizer'] Processing query: 'Deskripsikan seperti apa bentuk rumah Suku Bajo di atas air dan tata letak desa panggung mereka?'
   [Finished 'ResponseSynthesizer'] Successfully synthesized response: [...]

   Pipeline result: Berdasarkan teks tersebut, bentuk rumah dan tata letak desa Suku Bajo dapat dideskripsikan sebagai berikut:

   **Bentuk Rumah:**
   *   **Rumah Panggung di Atas Laut:** Ciri khas utama arsitektur Suku Bajo adalah rumah panggung yang dibangun langsung di atas permukaan air laut.
   *   **Adaptasi Maritim:** Desain rumah ini mencerminkan budaya maritim mereka yang kuat, di mana laut menjadi ruang hidup utama. Keunikan arsitektur ini bahkan menjadi inspirasi bagi pemukiman suku Metkayina dalam film *Avatar: The Way of Water*.

   **Tata Letak Desa:**
   *   **Pemukiman di Atas Air:** Mayoritas rumah warga dibangun berkelompok di atas air, seperti yang terlihat di Pulau Papan, kawasan Taman Nasional Kepulauan Togean.
   *   **Jembatan Penghubung:** Desa-desa mereka memiliki infrastruktur berupa jembatan panjang yang menghubungkan satu titik ke titik lain. Contohnya di Pulau Papan, terdapat jembatan sepanjang sekitar satu kilometer yang menghubungkan pulau tersebut dengan Pulau Malenge.
   *   **Pusat Kegiatan (Landmark):** Di tengah desa, terdapat area tertentu yang menjadi pusat interaksi sosial, seperti **Puncak Batu Karang** di Desa Pulau Papan. Tempat ini berfungsi sebagai area bermain bagi anak-anak suku Bajo dan tempat berinteraksi dengan wisatawan.
   *   **Integrasi dengan Daratan:** Meskipun tinggal di atas air, pemukiman mereka kini mulai membaur dengan daratan dan suku-suku lain, namun tetap mempertahankan identitas rumah panggung di atas laut sebagai tempat tinggal utama.
   ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/simple-image-rag-pipeline).
