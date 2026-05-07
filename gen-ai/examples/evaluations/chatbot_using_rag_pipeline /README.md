## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/001_your_first_rag_pipeline
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
    EMBEDDING_MODEL="text-embedding-3-small"
    LANGUAGE_MODEL="openai/gpt-5-nano"
    GOOGLE_API_KEY="..."
    ```

4. **Index the dataset**

   ```bash
   uv run indexer.py
   ```

5. **Run the example**

   ```bash
   uv run pipeline.py
   ```

6. **Expected Output**

   You should see a response similar to the following:

   ```log
   2025-10-10T16:14:35 DEBUG    [BasicVectorRetriever] [Start 'BasicVectorRetriever'] Processing input:
                                    - query: 'Give me nocturnal creatures from the dataset'                                                                                              
                                    - top_k: 5        
   2025-10-10T16:14:35 DEBUG    [BasicVectorRetriever] [Finished 'BasicVectorRetriever'] Successfully retrieved 5 chunks.
                                 - Rank: 1    
                                    ID: db9c9b9b-3294-4dd7-963a-068609c59da0   
                                    Content: The Luminafox is a nocturnal creature inhabiting t...                                    
                                    Score: 0.46340865561317823
                                    Metadata:         
                                    - name: Luminafox
                                 - Rank: 2        
                                    ID: 9ccb874b-5927-4b52-a67f-194666f92a1b  
                                    Content: The Dusk Panther prowls the twilight forests of Sh...
                                    Score: 0.45421676886176693
                                    Metadata: 
                                    - name: Dusk Panther   
                                 - Rank: 3                         
                                    ID: dff85b13-950c-424c-9312-fc086bd96086
                                    Content: The Gloombat flits through the dark caverns of Dus...          
                                    Score: 0.443562629568115    
                                    Metadata:     
                                    - name: Gloombat           
                                 - Rank: 4       
                                    ID: a38c7e84-78e2-4431-af77-c415e103b0fd   
                                    Content: The Moonstalker is a nocturnal predator prowling t...
                                    Score: 0.4423182992927307
                                    Metadata:
                                    - name: Moonstalker 
                                 - Rank: 5
                                    ID: 95ea2f37-3fa7-43d2-9049-bed203fa71cf 
                                    Content: The Glowhopper is an insect-like creature residing...
                                    Score: 0.423173318343201
                                    Metadata:
                                    - name: Glowhopper         
   2025-10-10T16:14:35 DEBUG    [ResponseSynthesizer] [Start 'ResponseSynthesizer'] Processing query: 'Give me nocturnal creatures from the dataset'                                                       
   2025-10-10T16:14:41 DEBUG    [ResponseSynthesizer] [Finished 'ResponseSynthesizer'] Successfully synthesized response: 
                              'Nocturnal creatures in the dataset:\n- Luminafox — glow-in-the-dark fur; inhabits luminescent forests of Nyxland.\n- Dusk Panther —                     
                              prowls twilight forests of Shadowglade; stealthy hunter.\n- Gloombat — flits through dark caverns of Dusk Hollow; echolocation                           
                              navigator.\n- Moonstalker — stalks the silver dunes of Lunar Plains; reflective coat aids camouflage.\n- Glowhopper — resident of                        
                              luminescent marshes in Lumina Bog; hops with light-emitting trails.'                                                                                     
   Pipeline result: Nocturnal creatures in the dataset:
   - Luminafox — glow-in-the-dark fur; inhabits luminescent forests of Nyxland.
   - Dusk Panther — prowls twilight forests of Shadowglade; stealthy hunter.
   - Gloombat — flits through dark caverns of Dusk Hollow; echolocation navigator.
   - Moonstalker — stalks the silver dunes of Lunar Plains; reflective coat aids camouflage.
   - Glowhopper — resident of luminescent marshes in Lumina Bog; hops with light-emitting trails.

   {'generation': {'aggregate_explanation': 'The following metrics failed to meet expectations:\n1. Completeness is 0.5 (should be >= 1)', 'aggregate_success': False, 'aggregate_score': 0.8333333333333334, 'completeness': {'score': 0.5, 'explanation': "The minimum key facts are: Luminafox, Dusk Panther, Gloombat, Moonstalker, and Glowhopper. The generated response correctly identifies Luminafox as a nocturnal creature. It mentions Dusk Panther and Gloombat in the notes but expresses uncertainty about their nocturnal status, whereas the expected output confirms them as part of the dataset's nocturnal creatures. Furthermore, Moonstalker and Glowhopper are completely missing from the response. Per Step 5C Coverage Rule, because some minimum key facts are matched but several others are missing, the response receives a partial score.", 'rubric_score': 2, 'success': False, 'threshold': 1.0, 'strict_mode': False, 'higher_is_better': True, 'model_id': 'google/gemini-3-flash-preview'}, 'redundancy': {'score': 0.0, 'explanation': 'The response is concise and contains no meaningful redundancy. Each creature mentioned (Luminafox, Dusk Panther, and Gloombat) is presented with unique information regarding its status in the dataset, and no sentences or ideas are repeated or paraphrased.', 'rubric_score': 1, 'success': True, 'threshold': 0.5, 'strict_mode': False, 'higher_is_better': False, 'model_id': 'google/gemini-3-flash-preview'}, 'groundedness': {'score': 1.0, 'explanation': "The response accurately identifies the Luminafox as the only creature explicitly labeled as 'nocturnal' in the context. It also correctly clarifies that while the Dusk Panther and Gloombat are associated with twilight or dark environments, the specific label 'nocturnal' is not applied to them in the text, which is a grounded observation based on the provided data.", 'rubric_score': 3, 'success': True, 'threshold': 1.0, 'strict_mode': False, 'higher_is_better': True, 'model_id': 'google/gemini-3-flash-preview'}, 'is_refusal': False}}

   ```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline).
