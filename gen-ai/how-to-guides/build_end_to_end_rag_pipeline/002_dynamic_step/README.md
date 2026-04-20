## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/002_dynamic_step
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

   When `use_knowledge_base` is set to `True`, you should see a response similar to the following:

   ```log
   2025-10-15T11:19:43 DEBUG    [BasicVectorRetriever] [Start                       component.py:130
                             'BasicVectorRetriever'] Processing input:                           
                                 - query: 'Give me nocturnal creatures from the                  
                             dataset'                                                            
                                 - top_k: 5                                                      
   2025-10-15T11:19:43 INFO     [OpenAIEMInvoker] Invoking 'OpenAIEMInvoker'       em_invoker.py:125
   2025-10-15T11:19:45 ERROR     Failed to send telemetry event CollectionQueryEvent:  posthog.py:61
                              capture() takes 1 positional argument but 3 were given              
   2025-10-15T11:19:45 DEBUG    [BasicVectorRetriever] [Finished                    component.py:130
                              'BasicVectorRetriever'] Successfully retrieved 5                    
                              chunks.                                                             
                                 - Rank: 1                                                         
                                    ID: ad636e30-7ba8-48f6-b52e-9b390207ca68                        
                                    Content: The Luminafox is a nocturnal creature                  
                              inhabiting t...                                                     
                                    Score: 0.46336014089183336                                      
                                    Metadata:                                                       
                                    - name: Luminafox                                             
                                 - Rank: 2                                                         
                                    ID: ad215dd9-1568-4c94-8734-86aee3f1a5a8                        
                                    Content: The Dusk Panther prowls the twilight                   
                              forests of Sh...                                                    
                                    Score: 0.4541605560513348                                       
                                    Metadata:                                                       
                                    - name: Dusk Panther                                          
                                 - Rank: 3                                                         
                                    ID: 96d317a1-a2df-43da-8d1d-373715fa9d71                        
                                    Content: The Gloombat flits through the dark                    
                              caverns of Dus...                                                   
                                    Score: 0.4435190881711845                                       
                                    Metadata:                                                       
                                    - name: Gloombat                                              
                                 - Rank: 4                                                         
                                    ID: 730a0a12-ce42-437e-821f-10ec2a6c6d7a                        
                                    Content: The Moonstalker is a nocturnal                         
                              predator prowling t...                                              
                                    Score: 0.44254742105417083                                      
                                    Metadata:                                                       
                                    - name: Moonstalker                                           
                                 - Rank: 5                                                         
                                    ID: 31f1bf5f-732d-4b4e-bcc4-56cb29b828ef                        
                                    Content: The Glowhopper is an insect-like                       
                              creature residing...                                                
                                    Score: 0.42312825178877955                                      
                                    Metadata:                                                       
                                    - name: Glowhopper                                            
   2025-10-15T11:19:45 DEBUG    [ResponseSynthesizer] [Start 'ResponseSynthesizer'] component.py:130
                              Processing query: 'Give me nocturnal creatures from                 
                              the dataset'                                                        
   2025-10-15T11:19:45 INFO     [OpenAILMInvoker] Invoking 'OpenAILMInvoker'       lm_invoker.py:252
   2025-10-15T11:19:55 INFO     [LMRequestProcessor] LM invocation       lm_request_processor.py:195
                              result:                                                             
                              '- Luminafox — a nocturnal creature with                            
                              glowing fur; navigates by bioluminescent                            
                              trails and hunts nocturnal insects.  \n-                            
                              Dusk Panther — prowls twilight/ night                               
                              forests; a stealthy hunter associated                               
                              with mystery and secrets.  \n- Gloombat                             
                              — flits through dark caverns; uses                                  
                              echolocation; active in the cave’s                                  
                              darkness.  \n- Moonstalker — a nocturnal                            
                              predator on the Lunar Plains; uses night                            
                              vision and silent movement.  \n-                                    
                              Glowhopper — resides in bioluminescent                              
                              marshes; glows to attract pollinators                               
                              and guides travelers in darkness.'                                  
   2025-10-15T11:19:55 DEBUG    [ResponseSynthesizer] [Finished                     component.py:130
                              'ResponseSynthesizer'] Successfully synthesized                     
                              response:                                                           
                              '- Luminafox — a nocturnal creature with glowing                    
                              fur; navigates by bioluminescent trails and hunts                   
                              nocturnal insects.  \n- Dusk Panther — prowls                       
                              twilight/ night forests; a stealthy hunter                          
                              associated with mystery and secrets.  \n- Gloombat                  
                              — flits through dark caverns; uses echolocation;                    
                              active in the cave’s darkness.  \n- Moonstalker — a                 
                              nocturnal predator on the Lunar Plains; uses night                  
                              vision and silent movement.  \n- Glowhopper —                       
                              resides in bioluminescent marshes; glows to attract                 
                              pollinators and guides travelers in darkness.'                      
   Pipeline result: - Luminafox — a nocturnal creature with glowing fur; navigates by bioluminescent trails and hunts nocturnal insects.  
   - Dusk Panther — prowls twilight/ night forests; a stealthy hunter associated with mystery and secrets.  
   - Gloombat — flits through dark caverns; uses echolocation; active in the cave’s darkness.  
   - Moonstalker — a nocturnal predator on the Lunar Plains; uses night vision and silent movement.  
   - Glowhopper — resides in bioluminescent marshes; glows to attract pollinators and guides travelers in darkness.
   ```

   Otherwise, you should see output like
   ```log
   2025-10-15T11:21:43 DEBUG    [ResponseSynthesizer] [Start 'ResponseSynthesizer'] component.py:130
                             Processing query: 'Give me nocturnal creatures from                 
                             the dataset'                                                        
   2025-10-15T11:21:43 WARNING  [StuffSynthesisStrategy] The         stuff_synthesis_strategy.py:101
                              'context' key is empty. Assigning                                   
                              default value: ''.                                                  
   2025-10-15T11:21:43 INFO     [OpenAILMInvoker] Invoking 'OpenAILMInvoker'       lm_invoker.py:252
   2025-10-15T11:21:55 INFO     [LMRequestProcessor] LM invocation       lm_request_processor.py:195
                              result:                                                             
                              'I don’t have your dataset here. If you                             
                              share the dataset or its structure                                  
                              (column names and a few rows), I can                                
                              return the nocturnal creatures. In the                              
                              meantime, here are quick ways to filter                             
                              for nocturnal animals in common                                     
                              formats.\n\nKey idea\n- Look for a field                            
                              that indicates activity period, e.g.,                               
                              activity_period or nocturnal                                        
                              (boolean).\n- If there isn’t a flag,                                
                              infer nocturnal from values like                                    
                              night/nighttime/overnight in the                                    
                              activity_period.\n\nPython (pandas)\n-                              
                              Using a boolean flag:\n  nocturnal_df =                             
                              df[df[\'nocturnal\'].astype(bool)]\n-                               
                              Inferring from activity_period:\n  mask                             
                              =                                                                   
                              df[\'activity_period\'].astype(str).str.                            
                              contains(r\'night|overnight|nocturnal\',                            
                                 case=False, na=False)\n  nocturnal_df =                            
                              df\n\nSQL\nSELECT * FROM dataset\nWHERE                             
                              nocturnal = TRUE\n   OR                                             
                              LOWER(activity_period) LIKE                                         
                              \'%night%\'\n   OR                                                  
                              LOWER(activity_period) LIKE                                         
                              \'%overnight%\';\n\nExcel/Sheets\n- If                              
                              you have activity_period:\n  Use a                                  
                              filter with criteria that contains                                  
                              night/overnight/nocturnal.\n- Or add a                              
                              helper column:\n                                                    
                              =IF(ISNUMBER(SEARCH("night",                                        
                              A2)),"Yes","No")\n  Filter where helper                             
                              column = Yes.\n\nIf you can paste:\n-                               
                              The dataset (or a small sample), or\n-                              
                              The exact column names (e.g., which                                 
                              column indicates nocturnal                                          
                              activity),\n\nI’ll generate the                                     
                              nocturnal subset for you.'                                          
   2025-10-15T11:21:55 DEBUG    [ResponseSynthesizer] [Finished                     component.py:130
                              'ResponseSynthesizer'] Successfully synthesized                     
                              response:                                                           
                              'I don’t have your dataset here. If you share the                   
                              dataset or its structure (column names and a few                    
                              rows), I can return the nocturnal creatures. In the                 
                              meantime, here are quick ways to filter for                         
                              nocturnal animals in common formats.\n\nKey idea\n-                 
                              Look for a field that indicates activity period,                    
                              e.g., activity_period or nocturnal (boolean).\n- If                 
                              there isn’t a flag, infer nocturnal from values                     
                              like night/nighttime/overnight in the                               
                              activity_period.\n\nPython (pandas)\n- Using a                      
                              boolean flag:\n  nocturnal_df =                                     
                              df[df[\'nocturnal\'].astype(bool)]\n- Inferring                     
                              from activity_period:\n  mask =                                     
                              df[\'activity_period\'].astype(str).str.contains(r\                 
                              'night|overnight|nocturnal\', case=False,                           
                              na=False)\n  nocturnal_df = df\n\nSQL\nSELECT *                     
                              FROM dataset\nWHERE nocturnal = TRUE\n   OR                         
                              LOWER(activity_period) LIKE \'%night%\'\n   OR                      
                              LOWER(activity_period) LIKE                                         
                              \'%overnight%\';\n\nExcel/Sheets\n- If you have                     
                              activity_period:\n  Use a filter with criteria that                 
                              contains night/overnight/nocturnal.\n- Or add a                     
                              helper column:\n  =IF(ISNUMBER(SEARCH("night",                      
                              A2)),"Yes","No")\n  Filter where helper column =                    
                              Yes.\n\nIf you can paste:\n- The dataset (or a                      
                              small sample), or\n- The exact column names (e.g.,                  
                              which column indicates nocturnal activity),\n\nI’ll                 
                              generate the nocturnal subset for you.'                             
   Pipeline result: I don’t have your dataset here. If you share the dataset or its structure (column names and a few rows), I can return the nocturnal creatures. In the meantime, here are quick ways to filter for nocturnal animals in common formats.

   Key idea
   - Look for a field that indicates activity period, e.g., activity_period or nocturnal (boolean).
   - If there isn’t a flag, infer nocturnal from values like night/nighttime/overnight in the activity_period.

   Python (pandas)
   - Using a boolean flag:
   nocturnal_df = df[df['nocturnal'].astype(bool)]
   - Inferring from activity_period:
   mask = df['activity_period'].astype(str).str.contains(r'night|overnight|nocturnal', case=False, na=False)
   nocturnal_df = df[mask]

   SQL
   SELECT * FROM dataset
   WHERE nocturnal = TRUE
      OR LOWER(activity_period) LIKE '%night%'
      OR LOWER(activity_period) LIKE '%overnight%';

   Excel/Sheets
   - If you have activity_period:
   Use a filter with criteria that contains night/overnight/nocturnal.
   - Or add a helper column:
   =IF(ISNUMBER(SEARCH("night", A2)),"Yes","No")
   Filter where helper column = Yes.

   If you can paste:
   - The dataset (or a small sample), or
   - The exact column names (e.g., which column indicates nocturnal activity),

   I’ll generate the nocturnal subset for you.
   
   ```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/).
