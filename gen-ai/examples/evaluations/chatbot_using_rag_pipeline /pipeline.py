"""Example script to build and run a simple RAG pipeline.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_evals.evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_pipeline.steps import step
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

load_dotenv()

# Create components
em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
    embedding=em_invoker,
)
retriever = BasicVectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.preset.stuff(os.getenv("LANGUAGE_MODEL"))

# Create the pipeline
retrieve_step = step(
    component=retriever,
    input_map={"query": "user_query", "top_k": "top_k"},
    output_state="chunks",
)
synthesize_step = step(
    component=response_synthesizer,
    input_map={"query": "user_query", "chunks": "chunks"},
    output_state="response",
)
e2e_pipeline = retrieve_step | synthesize_step

QUERY = "Give me nocturnal creatures from the dataset"

EXPECTED_OUTPUT = (
    "The nocturnal creatures in the dataset include the Luminafox, "
    "Dusk Panther, Gloombat, Moonstalker, and Glowhopper. "
    "They inhabit various dark environments such as caverns, twilight forests, "
    "and nocturnal plains, and exhibit traits like bioluminescence, echolocation, "
    "and stealth."
)


async def main():
    state = {"user_query": QUERY}
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)

    response = result["response"]
    chunks = result.get("chunks", [])
    retrieved_context = "\n".join(chunk.content for chunk in chunks)

    print(f"Pipeline result: {response}")

    # --- Evaluation ---
    print("\n--- Evaluation ---")
    test_case = LLMTestCase(
        input=QUERY,
        actual_output=response,
        expected_output=EXPECTED_OUTPUT,
        retrieved_context=retrieved_context,
    )

    judge_model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    evaluator = GEvalGenerationEvaluator(models=judge_model)
    eval_result = await evaluator.evaluate(test_case)

    print(eval_result)


if __name__ == "__main__":
    asyncio.run(main())
