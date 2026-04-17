## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/003_implement_semantic_routing
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
   2025-10-15T13:10:52 DEBUG    [AurelioSemanticRouter]    component.py:130
                             [Start                                     
                             'AurelioSemanticRouter']                   
                             Routing input source:                      
                             'Give me nocturnal                         
                             creatures from the                         
                             dataset'                                   
   2025-10-15T13:10:52 INFO     [OpenAIEMInvoker]         em_invoker.py:125
                              Invoking                                   
                              'OpenAIEMInvoker'                          
   2025-10-15T13:10:52 DEBUG    [AurelioSemanticRouter]    component.py:130
                              [Finished                                  
                              'AurelioSemanticRouter']                   
                              Successfully selected                      
                              route: 'knowledge_base'                    
   2025-10-15T13:10:52 DEBUG    [BasicVectorRetriever]     component.py:130
                              [Start                                     
                              'BasicVectorRetriever']                    
                              Processing input:                          
                                    - query: 'Give me                      
                              nocturnal creatures from                   
                              the dataset'                               
                                    - top_k: 5                             
   2025-10-15T13:10:52 INFO     [OpenAIEMInvoker]         em_invoker.py:125
                              Invoking                                   
                              'OpenAIEMInvoker'                          
   2025-10-15T13:10:53 DEBUG    [BasicVectorRetriever]     component.py:130
                              [Finished                                  
                              'BasicVectorRetriever']                    
                              Successfully retrieved 5                   
                              chunks.                                    
                                 - Rank: 1                                
                                    ID:                                    
                              fb945734-399f-4421-a41a-b7                 
                              cbcc56af4f                                 
                                    Content: The Luminafox                 
                              is a nocturnal creature                    
                              inhabiting t...                            
                                    Score:                                 
                              0.4633600132383856                         
                                    Metadata:                              
                                    - name: Luminafox                    
                                 - Rank: 2                                
                                    ID:                                    
                              62def957-4444-4dd8-bf71-51                 
                              7db6cc5adc                                 
                                    Content: The Luminafox                 
                              is a nocturnal creature                    
                              inhabiting t...                            
                                    Score:                                 
                              0.4633591942147865                         
                                    Metadata:                              
                                    - name: Luminafox                    
                                 - Rank: 3                                
                                    ID:                                    
                              909e3c85-7913-41ea-8cb3-a5                 
                              99ffe06e1c                                 
                                    Content: The Dusk                      
                              Panther prowls the                         
                              twilight forests of Sh...                  
                                    Score:                                 
                              0.45417081376492274                        
                                    Metadata:                              
                                    - name: Dusk Panther                 
                                 - Rank: 4                                
                                    ID:                                    
                              c30b53c7-8680-49fd-87ef-3f                 
                              991d2b82de                                 
                                    Content: The Dusk                      
                              Panther prowls the                         
                              twilight forests of Sh...                  
                                    Score:                                 
                              0.4541605602021751                         
                                    Metadata:                              
                                    - name: Dusk Panther                 
                                 - Rank: 5                                
                                    ID:                                    
                              d9f31742-4f7b-4ec4-9809-c0                 
                              828e2511a6                                 
                                    Content: The Gloombat                  
                              flits through the dark                     
                              caverns of Dus...                          
                                    Score:                                 
                              0.44351912363239404                        
                                    Metadata:                              
                                    - name: Gloombat                     
   2025-10-15T13:10:53 DEBUG    [ResponseSynthesizer]      component.py:130
                              [Start                                     
                              'ResponseSynthesizer']                     
                              Processing query: 'Give me                 
                              nocturnal creatures from                   
                              the dataset'                               
   2025-10-15T13:10:53 INFO     [OpenAILMInvoker]         lm_invoker.py:252
                              Invoking                                   
                              'OpenAILMInvoker'                          
   2025-10-15T13:11:05 INFO     [LMRequestProce lm_request_processor.py:195
                              ssor] LM                                   
                              invocation                                 
                              result:                                    
                              '- Luminafox —                             
                              explicitly                                 
                              described as                               
                              nocturnal,                                 
                              glowing in the                             
                              dark and using                             
                              bioluminescent                             
                              trails.\n\nNote                            
                              : The Dusk                                 
                              Panther is                                 
                              described as a                             
                              twilight                                   
                              (crepuscular)                              
                              hunter, and the                            
                              Gloombat is                                
                              described in                               
                              dark caves but                             
                              not explicitly                             
                              labeled as                                 
                              nocturnal. If                              
                              you’d like, I                              
                              can categorize                             
                              by active times                            
                              more strictly.'                            
   2025-10-15T13:11:05 DEBUG    [ResponseSynthesizer]      component.py:130
                              [Finished                                  
                              'ResponseSynthesizer']                     
                              Successfully synthesized                   
                              response:                                  
                              '- Luminafox — explicitly                  
                              described as nocturnal,                    
                              glowing in the dark and                    
                              using bioluminescent                       
                              trails.\n\nNote: The Dusk                  
                              Panther is described as a                  
                              twilight (crepuscular)                     
                              hunter, and the Gloombat                   
                              is described in dark caves                 
                              but not explicitly labeled                 
                              as nocturnal. If you’d                     
                              like, I can categorize by                  
                              active times more                          
                              strictly.'                                 
   Pipeline result: - Luminafox — explicitly described as nocturnal, glowing in the dark and using bioluminescent trails.

   Note: The Dusk Panther is described as a twilight (crepuscular) hunter, and the Gloombat is described in dark caves but not explicitly labeled as nocturnal. If you’d like, I can categorize by active times more strictly.
   ```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/implement-semantic-routing).