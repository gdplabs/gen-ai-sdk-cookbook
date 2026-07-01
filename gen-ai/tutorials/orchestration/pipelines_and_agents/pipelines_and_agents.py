from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
# 1. Define a deterministic RAG Pipeline
retrieval_step = step(retrieval_component, name="retrieve")
generation_step = step(generation_component, name="generate")
rag_pipeline = Pipeline([retrieval_step, generation_step])
# 2. Convert the Pipeline into a Tool
rag_tool = rag_pipeline.as_tool(
    name="rag_search",
    description="Retrieves relevant context and generates answers for factual queries."
)
# 3. Give the Tool to an Agent
agent = Agent(
    name="rag-agent",
    instruction="Use rag_search for factual questions.",
    tools=[rag_tool],
)
# The Agent decides when to call the pipeline!
print(agent.run("What is LangGraph?"))
