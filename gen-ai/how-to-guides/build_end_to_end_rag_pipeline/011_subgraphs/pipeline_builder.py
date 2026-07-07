# Complete pipeline_builder.py
from typing import TypedDict
import asyncio
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step, subgraph

# [Include all the dummy component classes and state definitions from above]

class ModularRAGPipelineBuilder:
    """Modular RAG pipeline builder using subgraphs."""

    def build(self) -> Pipeline:
        """Build the main pipeline using subgraphs."""
        preprocessing_step = self._build_preprocessing_subgraph()
        retrieval_step = self._build_retrieval_subgraph()
        generation_step = self._build_generation_subgraph()

        pipeline = Pipeline(
            steps=[
                preprocessing_step,
                retrieval_step,
                generation_step,
            ],
            state_type=MainRAGState,
            recursion_limit=100,
        )

        return pipeline

    # [Include all the _build_*_subgraph methods from above]

# Test the pipeline
async def test_modular_pipeline():
    builder = ModularRAGPipelineBuilder()
    pipeline = builder.build()

    state = {
        "user_query": "What are some forest animals?",
    }

    config = {
        "top_k": 5,
        "debug": True,
    }

    result = await pipeline.invoke(state, config)
    print(f"Pipeline result: {result}")

if __name__ == "__main__":
    asyncio.run(test_modular_pipeline())
