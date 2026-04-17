## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/004_adding_document_references
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
   2025-10-15T12:44:09 DEBUG    [BasicVectorRetriever]     component.py:130
                             [Start                                     
                             'BasicVectorRetriever']                    
                             Processing input:                          
                                 - query: 'Give me                      
                             nocturnal creatures from                   
                             the dataset'                               
                                 - top_k: 5                             
   2025-10-15T12:44:09 INFO     [OpenAIEMInvoker]         em_invoker.py:125
                              Invoking                                   
                              'OpenAIEMInvoker'                          
   2025-10-15T12:44:11 ERROR     Failed to send telemetry     posthog.py:61
                              event CollectionQueryEvent:                
                              capture() takes 1 positional               
                              argument but 3 were given                  
   2025-10-15T12:44:11 DEBUG    [BasicVectorRetriever]     component.py:130
                              [Finished                                  
                              'BasicVectorRetriever']                    
                              Successfully retrieved 5                   
                              chunks.                                    
                                 - Rank: 1                                
                                    ID:                                    
                              ffe9bfbf-6065-480c-bded-27                 
                              6ac9994d72                                 
                                    Content: The Luminafox                 
                              is a nocturnal creature                    
                              inhabiting t...                            
                                    Score:                                 
                              0.4633599574686413                         
                                    Metadata:                              
                                    - name: Luminafox                    
                                 - Rank: 2                                
                                    ID:                                    
                              b91d6dfb-f177-48c9-84dd-a7                 
                              82b785ee0d                                 
                                    Content: The Dusk                      
                              Panther prowls the                         
                              twilight forests of Sh...                  
                                    Score:                                 
                              0.4541605560513348                         
                                    Metadata:                              
                                    - name: Dusk Panther                 
                                 - Rank: 3                                
                                    ID:                                    
                              05429706-c477-4804-a4e5-9d                 
                              a1ddf50632                                 
                                    Content: The Gloombat                  
                              flits through the dark                     
                              caverns of Dus...                          
                                    Score:                                 
                              0.4435190881711845                         
                                    Metadata:                              
                                    - name: Gloombat                     
                                 - Rank: 4                                
                                    ID:                                    
                              4965e21b-4780-4a76-9d6a-b7                 
                              0e4faf1da2                                 
                                    Content: The                           
                              Moonstalker is a nocturnal                 
                              predator prowling t...                     
                                    Score:                                 
                              0.44225796877897344                        
                                    Metadata:                              
                                    - name: Moonstalker                  
                                 - Rank: 5                                
                                    ID:                                    
                              d95382d7-2fdb-41cf-b741-ec                 
                              0ceaed732d                                 
                                    Content: The                           
                              Glowhopper is an                           
                              insect-like creature                       
                              residing...                                
                                    Score:                                 
                              0.42312825178877955                        
                                    Metadata:                              
                                    - name: Glowhopper                   
   2025-10-15T12:44:11 DEBUG    [ResponseSynthesizer]      component.py:130
                              [Start                                     
                              'ResponseSynthesizer']                     
                              Processing query: 'Give me                 
                              nocturnal creatures from                   
                              the dataset'                               
   2025-10-15T12:44:11 INFO     [OpenAILMInvoker]         lm_invoker.py:252
                              Invoking                                   
                              'OpenAILMInvoker'                          
   2025-10-15T12:44:29 INFO     [LMRequestProce lm_request_processor.py:195
                              ssor] LM                                   
                              invocation                                 
                              result:                                    
                              'Explicitly                                
                              nocturnal                                  
                              creatures in                               
                              the dataset:\n-                            
                              Luminafox\n-                               
                              Moonstalker\n\n                            
                              Note:\n- Dusk                              
                              Panther is                                 
                              described in                               
                              twilight (near                             
                              night), so it’s                            
                              closely                                    
                              associated with                            
                              night but not                              
                              explicitly                                 
                              labeled                                    
                              nocturnal.\n-                              
                              Gloombat and                               
                              Glowhopper                                 
                              aren’t                                     
                              explicitly                                 
                              described as                               
                              nocturnal in                               
                              their entries.'                            
   2025-10-15T12:44:29 DEBUG    [ResponseSynthesizer]      component.py:130
                              [Finished                                  
                              'ResponseSynthesizer']                     
                              Successfully synthesized                   
                              response:                                  
                              'Explicitly nocturnal                      
                              creatures in the                           
                              dataset:\n- Luminafox\n-                   
                              Moonstalker\n\nNote:\n-                    
                              Dusk Panther is described                  
                              in twilight (near night),                  
                              so it’s closely associated                 
                              with night but not                         
                              explicitly labeled                         
                              nocturnal.\n- Gloombat and                 
                              Glowhopper aren’t                          
                              explicitly described as                    
                              nocturnal in their                         
                              entries.'                                  
   2025-10-15T12:44:29 DEBUG    [SimilarityBasedReferenceF component.py:130
                              ormatter] [Start                           
                              'SimilarityBasedReferenceF                 
                              ormatter'] Formatting                      
                              references using 5                         
                              candidate chunks.                          
   2025-10-15T12:44:29 INFO     [OpenAIEMInvoker]         em_invoker.py:125
                              Invoking                                   
                              'OpenAIEMInvoker'                          
   2025-10-15T12:44:32 INFO     [OpenAIEMInvoker]         em_invoker.py:125
                              Invoking                                   
                              'OpenAIEMInvoker'                          
   2025-10-15T12:44:34 DEBUG    [SimilarityBasedReferenceF component.py:130
                              ormatter] [Finished                        
                              'SimilarityBasedReferenceF                 
                              ormatter'] Successfully                    
                              formatted references:                      
                              [Chunk(id=ffe9bfbf-6065-48                 
                              0c-bded-276ac9994d72,                      
                              content=The Luminafox is a                 
                              nocturnal creature                         
                              inhabiting t...,                           
                              metadata={'name':                          
                              'Luminafox'},                              
                              score=0.4633599574686413),                 
                              Chunk(id=b91d6dfb-f177-48c                 
                              9-84dd-a782b785ee0d,                       
                              content=The Dusk Panther                   
                              prowls the twilight                        
                              forests of Sh...,                          
                              metadata={'name': 'Dusk                    
                              Panther'},                                 
                              score=0.4541605560513348),                 
                              Chunk(id=05429706-c477-480                 
                              4-a4e5-9da1ddf50632,                       
                              content=The Gloombat flits                 
                              through the dark caverns                   
                              of Dus...,                                 
                              metadata={'name':                          
                              'Gloombat'},                               
                              score=0.4435190881711845),                 
                              Chunk(id=4965e21b-4780-4a7                 
                              6-9d6a-b70e4faf1da2,                       
                              content=The Moonstalker is                 
                              a nocturnal predator                       
                              prowling t...,                             
                              metadata={'name':                          
                              'Moonstalker'},                            
                              score=0.44225796877897344)                 
                              ,                                          
                              Chunk(id=d95382d7-2fdb-41c                 
                              f-b741-ec0ceaed732d,                       
                              content=The Glowhopper is                  
                              an insect-like creature                    
                              residing...,                               
                              metadata={'name':                          
                              'Glowhopper'},                             
                              score=0.42312825178877955)                 
                              ]                                          
   Pipeline result: Explicitly nocturnal creatures in the dataset:
   - Luminafox
   - Moonstalker

   Note:
   - Dusk Panther is described in twilight (near night), so it’s closely associated with night but not explicitly labeled nocturnal.
   - Gloombat and Glowhopper aren’t explicitly described as nocturnal in their entries.
   References: [Chunk(id=ffe9bfbf-6065-480c-bded-276ac9994d72, content=The Luminafox is a nocturnal creature inhabiting t..., metadata={'name': 'Luminafox'}, score=0.4633599574686413), Chunk(id=b91d6dfb-f177-48c9-84dd-a782b785ee0d, content=The Dusk Panther prowls the twilight forests of Sh..., metadata={'name': 'Dusk Panther'}, score=0.4541605560513348), Chunk(id=05429706-c477-4804-a4e5-9da1ddf50632, content=The Gloombat flits through the dark caverns of Dus..., metadata={'name': 'Gloombat'}, score=0.4435190881711845), Chunk(id=4965e21b-4780-4a76-9d6a-b70e4faf1da2, content=The Moonstalker is a nocturnal predator prowling t..., metadata={'name': 'Moonstalker'}, score=0.44225796877897344), Chunk(id=d95382d7-2fdb-41cf-b741-ec0ceaed732d, content=The Glowhopper is an insect-like creature residing..., metadata={'name': 'Glowhopper'}, score=0.42312825178877955)]
   
   ```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/adding-document-references).
