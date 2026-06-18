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
   2026-06-17T14:31:45 DEBUG    [VectorRetriever] [Start 'VectorRetriever'] Processing input:                                                                   
                                 - query: 'Penilaian spesifik apa yang harus diselesaikan sebagai syarat bagi pasien untuk bertransisi dari fase Inpatient                   
                             NARP menuju Community NARP?'                                                                                                                    
                                 - top_k: 5                                                                                                                                  
   2026-06-17T14:31:46 INFO     [OpenAIEMInvoker] Invoking 'openai/text-embedding-3-small'                                                                     
   2026-06-17T14:31:47 DEBUG    [VectorRetriever] [Finished 'VectorRetriever'] Successfully produced output:                                                    
                              [Chunk(id=43ec3b46bb3da168995fe6dde5f060b4904768a0d35961765c0bd8bbb8b1aead-StructuredElementChunker-1800-360-4000-0-markdown-Tr                 
                              ue-35, content=Diagram alir ini menunjuk..., metadata={'chunk_id': '43ec3b46bb3da168995fe6dde...', 'file_id':                                   
                              '43ec3b46bb3da168995fe6dde...', 'heading 1': 'A variation of the Non-Ac...', 'heading 2': 'Pathways Service', 'heading 3':                      
                              'About the Contract', 'heading 4': 'Patient scenarios for Non...', 'layout_height': 842, 'layout_width': 595,                                   
                              'loaded_datetime': '2026-06-17 14:01:08', 'next_chunk': '43ec3b46bb3da168995fe6dde...', 'page_number': 21, 'previous_chunk':                    
                              '43ec3b46bb3da168995fe6dde...', 'source': 'NARP-Operational-Guide-tr...', 'source_type': 'pdf', 'structure': 'image', 'title':                  
                              'Operational Guidelines'}, score=0.659183864516435),                                                                                            
                              Chunk(id=43ec3b46bb3da168995fe6dde5f060b4904768a0d35961765c0bd8bbb8b1aead-StructuredElementChunker-1800-360-4000-0-markdown-Tru                 
                              e-37, content=Diagram alur ini menampil..., metadata={'chunk_id': '43ec3b46bb3da168995fe6dde...', 'file_id':                                    
                              '43ec3b46bb3da168995fe6dde...', 'heading 1': 'A variation of the Non-Ac...', 'heading 2': 'Pathways Service', 'heading 3':                      
                              'About the Contract', 'heading 4': 'Patient scenarios for Non...', 'heading 6': 'Figure 4: Transitional an...',                                 
                              'layout_height': 842, 'layout_width': 595, 'loaded_datetime': '2026-06-17 14:04:27', 'next_chunk':                                              
                              '43ec3b46bb3da168995fe6dde...', 'page_number': 22, 'previous_chunk': '43ec3b46bb3da168995fe6dde...', 'source':                                  
                              'NARP-Operational-Guide-tr...', 'source_type': 'pdf', 'structure': 'image', 'title': 'Operational Guidelines'},                                 
                              score=0.6363033053767015),                                                                                                                      
                              Chunk(id=43ec3b46bb3da168995fe6dde5f060b4904768a0d35961765c0bd8bbb8b1aead-StructuredElementChunker-1800-360-4000-0-markdown-Tru                 
                              e-37, content=Diagram ini mengilustrasi..., metadata={'chunk_id': '43ec3b46bb3da168995fe6dde...', 'file_id':                                    
                              '43ec3b46bb3da168995fe6dde...', 'heading 1': 'A variation of the Non-Ac...', 'heading 2': 'Pathways Service', 'heading 3':                      
                              'About the Contract', 'heading 4': 'Patient scenarios for Non...', 'heading 6': 'Figure 4: Transitional an...',                                 
                              'layout_height': 842, 'layout_width': 595, 'loaded_datetime': '2026-06-17 13:54:33', 'next_chunk':                                              
                              '43ec3b46bb3da168995fe6dde...', 'page_number': 22, 'previous_chunk': '43ec3b46bb3da168995fe6dde...', 'source':                                  
                              'NARP-Operational-Guide-tr...', 'source_type': 'pdf', 'title': 'Operational Guidelines'}, score=0.6350571780557253),                            
                              Chunk(id=43ec3b46bb3da168995fe6dde5f060b4904768a0d35961765c0bd8bbb8b1aead-StructuredElementChunker-1800-360-4000-0-markdown-Tru                 
                              e-31, content=Diagram ini mengilustrasi..., metadata={'chunk_id': '43ec3b46bb3da168995fe6dde...', 'file_id':                                    
                              '43ec3b46bb3da168995fe6dde...', 'heading 1': 'A variation of the Non-Ac...', 'heading 2': 'Pathways Service', 'heading 3':                      
                              'About the Contract', 'heading 4': 'Patient scenarios for Non...', 'layout_height': 842, 'layout_width': 595,                                   
                              'loaded_datetime': '2026-06-17 14:01:08', 'next_chunk': '43ec3b46bb3da168995fe6dde...', 'page_number': 19, 'previous_chunk':                    
                              '43ec3b46bb3da168995fe6dde...', 'source': 'NARP-Operational-Guide-tr...', 'source_type': 'pdf', 'structure': 'image', 'title':                  
                              'Operational Guidelines'}, score=0.6325470480871898),                                                                                           
                              Chunk(id=43ec3b46bb3da168995fe6dde5f060b4904768a0d35961765c0bd8bbb8b1aead-StructuredElementChunker-1800-360-4000-0-markdown-Tru                 
                              e-35, content=Diagram ini mengilustrasi..., metadata={'chunk_id': '43ec3b46bb3da168995fe6dde...', 'file_id':                                    
                              '43ec3b46bb3da168995fe6dde...', 'heading 1': 'A variation of the Non-Ac...', 'heading 2': 'Pathways Service', 'heading 3':                      
                              'About the Contract', 'heading 4': 'Patient scenarios for Non...', 'layout_height': 842, 'layout_width': 595,                                   
                              'loaded_datetime': '2026-06-17 13:54:33', 'next_chunk': '43ec3b46bb3da168995fe6dde...', 'page_number': 21, 'previous_chunk':                    
                              '43ec3b46bb3da168995fe6dde...', 'source': 'NARP-Operational-Guide-tr...', 'source_type': 'pdf', 'title': 'Operational                           
                              Guidelines'}, score=0.6273489250897815)]                                                                                                        
   2026-06-17T14:31:47 DEBUG    [ResponseSynthesizer] [Start 'ResponseSynthesizer'] Processing query: 'Penilaian spesifik apa yang harus diselesaikan sebagai   
                              syarat bagi pasien untuk bertransisi dari fase Inpatient NARP menuju Community NARP?'                                                           
   2026-06-17T14:31:47 INFO     [GoogleLMInvoker] Invoking 'google/gemini-3-flash-preview'                                                                     
   2026-06-17T14:31:47 INFO      AFC is enabled with max remote calls: 10.                                                                                        
   2026-06-17T14:31:52 INFO     [LMRequestProcessor] LM invocation result:                                                                           
                              LMOutput(                                                                                                                                       
                                    outputs=[                                                                                                                                   
                                       LMOutputItem(type='text', output='Berdasarkan diagram alir yang dijelaskan dalam konteks tersebut, penilaian                            
                              spesifik yang harus diselesaikan untuk bertransisi dari fase Inpatient NARP menuju Community NARP adalah:\n\n1.                                 
                              **interRAI Acute Care (AC) Admission Assessment** atau **Inpatient Profiling Tool**: Dilakukan pada fase Inpatient                              
                              NARP untuk menilai kondisi pasien secara komprehensif.\n2.  **Community Profiling Tool**: Digunakan sebagai dasar                               
                              penentuan klinis sebelum pasien masuk ke layanan Community NARP.\n3.  **Input Client Data ke NARP Spreadsheet**:                                
                              Sebagai langkah dokumentasi wajib yang dilakukan pada setiap tahap transisi layanan.\n\nSecara singkat, transisi ini                            
                              melibatkan penyelesaian penilaian rawat inap (interRAI AC/Inpatient Profiling Tool) dan penilaian kesiapan komunitas                            
                              (Community Profiling Tool) serta pencatatan data ke dalam spreadsheet NARP.')                                                                   
                                    ]                                                                                                                                           
                              )                                                                                                                                               
   2026-06-17T14:31:52 DEBUG    [ResponseSynthesizer] [Finished 'ResponseSynthesizer'] Successfully synthesized response:                                       
                              'Berdasarkan diagram alir yang dijelaskan dalam konteks tersebut, penilaian spesifik yang harus diselesaikan untuk bertransisi                  
                              dari fase Inpatient NARP menuju Community NARP adalah:\n\n1.  **interRAI Acute Care (AC) Admission Assessment** atau                            
                              **Inpatient Profiling Tool**: Dilakukan pada fase Inpatient NARP untuk menilai kondisi pasien secara komprehensif.\n2.                          
                              **Community Profiling Tool**: Digunakan sebagai dasar penentuan klinis sebelum pasien masuk ke layanan Community NARP.\n3.                      
                              **Input Client Data ke NARP Spreadsheet**: Sebagai langkah dokumentasi wajib yang dilakukan pada setiap tahap transisi                          
                              layanan.\n\nSecara singkat, transisi ini melibatkan penyelesaian penilaian rawat inap (interRAI AC/Inpatient Profiling Tool)                    
                              dan penilaian kesiapan komunitas (Community Profiling Tool) serta pencatatan data ke dalam spreadsheet NARP.'
   Pipeline result: Berdasarkan diagram alir yang dijelaskan dalam konteks tersebut, penilaian spesifik yang harus diselesaikan untuk bertransisi dari fase Inpatient NARP menuju Community NARP adalah:

   1.  interRAI Acute Care (AC) Admission Assessment atau Inpatient Profiling Tool: Dilakukan pada fase Inpatient NARP untuk menilai kondisi pasien secara komprehensif.
   2.  Community Profiling Tool: Digunakan sebagai dasar penentuan klinis sebelum pasien masuk ke layanan Community NARP.
   3.  Input Client Data ke NARP Spreadsheet: Sebagai langkah dokumentasi wajib yang dilakukan pada setiap tahap transisi layanan.

   Secara singkat, transisi ini melibatkan penyelesaian penilaian rawat inap (interRAI AC/Inpatient Profiling Tool) dan penilaian kesiapan komunitas (Community Profiling Tool) serta pencatatan data ke dalam spreadsheet NARP.
   ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/image-search-pipeline).
