## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/006_query_transformation
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
      2025-10-15T21:56:53 DEBUG    [OneToOneQueryTransformer] [Start 'OneToOneQueryTransformer'] Processing query:     component.py:130
                              'Give me nocturnal creatures from the dataset'                                                      
      2025-10-15T21:56:53 WARNING  [LMRequestProcessor] The `prompt_kwargs` parameter is deprecated and     lm_request_processor.py:160
                              will be removed in v0.6. Please pass the prompt kwargs as keyword                                   
                              arguments instead.                                                                                  
      2025-10-15T21:56:53 INFO     [OpenAILMInvoker] Invoking 'OpenAILMInvoker'                                       lm_invoker.py:252
      2025-10-15T21:56:57 INFO     [LMRequestProcessor] LM invocation result:                               lm_request_processor.py:195
                              'List nocturnal animals from the dataset.'                                                          
      2025-10-15T21:56:57 DEBUG    [OneToOneQueryTransformer] [Finished 'OneToOneQueryTransformer'] Successfully       component.py:130
                              produced 1 result(s):                                                                               
                                    - 'List nocturnal animals from the dataset.'                                                    
      2025-10-15T21:56:57 DEBUG    [BasicVectorRetriever] [Start 'BasicVectorRetriever'] Processing input:             component.py:130
                                    - query: 'Give me nocturnal creatures from the dataset'                                         
                                    - top_k: 5                                                                                      
      2025-10-15T21:56:57 INFO     [OpenAIEMInvoker] Invoking 'OpenAIEMInvoker'                                       em_invoker.py:125
      2025-10-15T21:56:58 ERROR     Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional     posthog.py:61
                              argument but 3 were given                                                                           
      2025-10-15T21:56:58 DEBUG    [BasicVectorRetriever] [Finished 'BasicVectorRetriever'] Successfully retrieved 5   component.py:130
                              chunks.                                                                                             
                                    - Rank: 1                                                                                         
                                    ID: ffe9bfbf-6065-480c-bded-276ac9994d72                                                        
                                    Content: The Luminafox is a nocturnal creature inhabiting t...                                  
                                    Score: 0.4633599574686413                                                                       
                                    Metadata:                                                                                       
                                    - name: Luminafox                                                                             
                                    - Rank: 2                                                                                         
                                    ID: b91d6dfb-f177-48c9-84dd-a782b785ee0d                                                        
                                    Content: The Dusk Panther prowls the twilight forests of Sh...                                  
                                    Score: 0.4541605560513348                                                                       
                                    Metadata:                                                                                       
                                    - name: Dusk Panther                                                                          
                                    - Rank: 3                                                                                         
                                    ID: 05429706-c477-4804-a4e5-9da1ddf50632                                                        
                                    Content: The Gloombat flits through the dark caverns of Dus...                                  
                                    Score: 0.4435190881711845                                                                       
                                    Metadata:                                                                                       
                                    - name: Gloombat                                                                              
                                    - Rank: 4                                                                                         
                                    ID: 4965e21b-4780-4a76-9d6a-b70e4faf1da2                                                        
                                    Content: The Moonstalker is a nocturnal predator prowling t...                                  
                                    Score: 0.44225796877897344                                                                      
                                    Metadata:                                                                                       
                                    - name: Moonstalker                                                                           
                                    - Rank: 5                                                                                         
                                    ID: d95382d7-2fdb-41cf-b741-ec0ceaed732d                                                        
                                    Content: The Glowhopper is an insect-like creature residing...                                  
                                    Score: 0.42312825178877955                                                                      
                                    Metadata:                                                                                       
                                    - name: Glowhopper                                                                            
      2025-10-15T21:56:58 DEBUG    [ResponseSynthesizer] [Start 'ResponseSynthesizer'] Processing query: 'Give me      component.py:130
                              nocturnal creatures from the dataset'                                                               
      2025-10-15T21:56:58 INFO     [OpenAILMInvoker] Invoking 'OpenAILMInvoker'                                       lm_invoker.py:252
      2025-10-15T21:57:07 INFO     [LMRequestProcessor] LM invocation result:                               lm_request_processor.py:195
                              'Nocturnal creatures in the dataset:\n- Luminafox\n- Dusk Panther\n-                                
                              Moonstalker'                                                                                        
      2025-10-15T21:57:07 DEBUG    [ResponseSynthesizer] [Finished 'ResponseSynthesizer'] Successfully synthesized     component.py:130
                              response:                                                                                           
                              'Nocturnal creatures in the dataset:\n- Luminafox\n- Dusk Panther\n- Moonstalker'                   
      Pipeline result: Nocturnal creatures in the dataset:
      - Luminafox
      - Dusk Panther
      - Moonstalker
   
   ```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/query-transformation).
