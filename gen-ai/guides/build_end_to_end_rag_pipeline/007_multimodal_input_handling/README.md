## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/examples/e2e_rag_pipeline/007_multimodal_input_handling
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
      2025-10-15T18:19:56 DEBUG    [BasicVectorRetriever] [Start 'BasicVectorRetriever'] Processing input:             component.py:130
                                    - query: 'Aquatic animals'                                                                      
                                    - top_k: 5                                                                                      
      2025-10-15T18:19:56 INFO     [OpenAIEMInvoker] Invoking 'OpenAIEMInvoker'                                       em_invoker.py:125
      2025-10-15T18:19:57 ERROR     Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional     posthog.py:61
                              argument but 3 were given                                                                           
      2025-10-15T18:19:57 DEBUG    [BasicVectorRetriever] [Finished 'BasicVectorRetriever'] Successfully retrieved 5   component.py:130
                              chunks.                                                                                             
                                    - Rank: 1                                                                                         
                                    ID: 052499a5-fb09-43dc-b1cd-9e0094f3aa38                                                        
                                    Content: The Aquaflare is a marine creature found in the fi...                                  
                                    Score: 0.4562330844248475                                                                       
                                    Metadata:                                                                                       
                                    - name: Aquaflare                                                                             
                                    - Rank: 2                                                                                         
                                    ID: 4b52c6b9-be02-4f7d-8e5a-897274d82392                                                        
                                    Content: The Aquaglow Jelly drifts in the tranquil depths o...                                  
                                    Score: 0.4440772150126268                                                                       
                                    Metadata:                                                                                       
                                    - name: Aquaglow Jelly                                                                        
                                    - Rank: 3                                                                                         
                                    ID: e2224505-fe0a-44f4-a629-20918bc3d352                                                        
                                    Content: The Starburst Lionfish glides through the coral re...                                  
                                    Score: 0.4364320567641672                                                                       
                                    Metadata:                                                                                       
                                    - name: Starburst Lionfish                                                                    
                                    - Rank: 4                                                                                         
                                    ID: c54e9744-f933-4517-b113-954258345d2e                                                        
                                    Content: Inhabiting the swirling waters of Maelstrom Sea, t...                                  
                                    Score: 0.43380524927485065                                                                      
                                    Metadata:                                                                                       
                                    - name: Whirlpool Serpent                                                                     
                                    - Rank: 5                                                                                         
                                    ID: f718ba0f-9cd2-461a-8ff4-9b6b096ca3b1                                                        
                                    Content: The Luminescent Koi swims in the serene ponds of M...                                  
                                    Score: 0.4294435669552394                                                                       
                                    Metadata:                                                                                       
                                    - name: Luminescent Koi                                                                       
      2025-10-15T18:19:57 DEBUG    [ResponseSynthesizer] [Start 'ResponseSynthesizer'] Processing query: 'Aquatic      component.py:130
                              animals'                                                                                            
      2025-10-15T18:19:57 INFO     [OpenAILMInvoker] Invoking 'OpenAILMInvoker'                                       lm_invoker.py:252
      2025-10-15T18:20:23 INFO     [LMRequestProcessor] LM invocation result:                               lm_request_processor.py:195
                              'Here are some imaginative aquatic animals, plus a dog-inspired one that                            
                              fits the image you shared:\n\n- Aquaflare: A marine creature from                                   
                              Pyronia’s volcanic isles. Resembles a dolphin-salamander blend, with                                
                              heat-resistant scales that shimmer in fiery hues. Feeds on                                          
                              magma-dwelling microbes, can dive into underwater lava flows, and                                   
                              communicates with ultrasonic clicks.\n\n- Aquaglow Jelly: A translucent                             
                              jellyfish in Azure Lake that emits a gentle blue bioluminescence.                                   
                              Filters microscopic organisms through delicate tentacles and                                        
                              synchronizes light displays in swarms to illuminate the depths.\n\n-                                
                              Starburst Lionfish: Glides through Celestial Sea reefs. Fins flare into                             
                              a starburst pattern with luminescent tips; uses flashy displays to                                  
                              confuse prey. Mildly toxic spines deter predators; typically solitary                               
                              and plays a role in reef balance.\n\n- Whirlpool Serpent: Dwells in                                 
                              Maelstrom Sea. Long, flexible body with rapidly rotating fins that                                  
                              generate whirlpools to trap schools of fish. Color-shifting scales                                  
                              provide camouflage; communicates with pulsating body light patterns and                             
                              is considered an omen by sailors.\n\n- Luminescent Koi: Sculpts tranquil                            
                              Moonshadow Gardens’ ponds with glow-in-the-dark scales. Feeds on aquatic                            
                              plants and tiny insects; gathers in groups during full moon to create                               
                              floating displays of light for serenity and ecological balance.\n\n- Sea                            
                              Retriever (dog-inspired aquatic creature): A medium-sized, canine-like                              
                              marine mammal with a sleek, water-repellent coat of kelp-threads and                                
                              webbed paws. Feeds on small fish and crustaceans, using gentle                                      
                              dunt-click communication and shallow-water foraging. Thrives near                                   
                              coastal rocks and reefs, often seen riding the edge of waves with a                                 
                              calm, friendly demeanor—an emblem of harmony between land and sea.'                                 
      2025-10-15T18:20:23 DEBUG    [ResponseSynthesizer] [Finished 'ResponseSynthesizer'] Successfully synthesized     component.py:130
                              response:                                                                                           
                              'Here are some imaginative aquatic animals, plus a dog-inspired one that fits the                   
                              image you shared:\n\n- Aquaflare: A marine creature from Pyronia’s volcanic isles.                  
                              Resembles a dolphin-salamander blend, with heat-resistant scales that shimmer in                    
                              fiery hues. Feeds on magma-dwelling microbes, can dive into underwater lava flows,                  
                              and communicates with ultrasonic clicks.\n\n- Aquaglow Jelly: A translucent                         
                              jellyfish in Azure Lake that emits a gentle blue bioluminescence. Filters                           
                              microscopic organisms through delicate tentacles and synchronizes light displays in                 
                              swarms to illuminate the depths.\n\n- Starburst Lionfish: Glides through Celestial                  
                              Sea reefs. Fins flare into a starburst pattern with luminescent tips; uses flashy                   
                              displays to confuse prey. Mildly toxic spines deter predators; typically solitary                   
                              and plays a role in reef balance.\n\n- Whirlpool Serpent: Dwells in Maelstrom Sea.                  
                              Long, flexible body with rapidly rotating fins that generate whirlpools to trap                     
                              schools of fish. Color-shifting scales provide camouflage; communicates with                        
                              pulsating body light patterns and is considered an omen by sailors.\n\n-                            
                              Luminescent Koi: Sculpts tranquil Moonshadow Gardens’ ponds with glow-in-the-dark                   
                              scales. Feeds on aquatic plants and tiny insects; gathers in groups during full                     
                              moon to create floating displays of light for serenity and ecological balance.\n\n-                 
                              Sea Retriever (dog-inspired aquatic creature): A medium-sized, canine-like marine                   
                              mammal with a sleek, water-repellent coat of kelp-threads and webbed paws. Feeds on                 
                              small fish and crustaceans, using gentle dunt-click communication and shallow-water                 
                              foraging. Thrives near coastal rocks and reefs, often seen riding the edge of waves                 
                              with a calm, friendly demeanor—an emblem of harmony between land and sea.'                          
      Pipeline result: Here are some imaginative aquatic animals, plus a dog-inspired one that fits the image you shared:

      - Aquaflare: A marine creature from Pyronia’s volcanic isles. Resembles a dolphin-salamander blend, with heat-resistant scales that shimmer in fiery hues. Feeds on magma-dwelling microbes, can dive into underwater lava flows, and communicates with ultrasonic clicks.

      - Aquaglow Jelly: A translucent jellyfish in Azure Lake that emits a gentle blue bioluminescence. Filters microscopic organisms through delicate tentacles and synchronizes light displays in swarms to illuminate the depths.

      - Starburst Lionfish: Glides through Celestial Sea reefs. Fins flare into a starburst pattern with luminescent tips; uses flashy displays to confuse prey. Mildly toxic spines deter predators; typically solitary and plays a role in reef balance.

      - Whirlpool Serpent: Dwells in Maelstrom Sea. Long, flexible body with rapidly rotating fins that generate whirlpools to trap schools of fish. Color-shifting scales provide camouflage; communicates with pulsating body light patterns and is considered an omen by sailors.

      - Luminescent Koi: Sculpts tranquil Moonshadow Gardens’ ponds with glow-in-the-dark scales. Feeds on aquatic plants and tiny insects; gathers in groups during full moon to create floating displays of light for serenity and ecological balance.

      - Sea Retriever (dog-inspired aquatic creature): A medium-sized, canine-like marine mammal with a sleek, water-repellent coat of kelp-threads and webbed paws. Feeds on small fish and crustaceans, using gentle dunt-click communication and shallow-water foraging. Thrives near coastal rocks and reefs, often seen riding the edge of waves with a calm, friendly demeanor—an emblem of harmony between land and sea.
   
   ```

## 🚀 Reference
These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/multimodal-input-handling).
