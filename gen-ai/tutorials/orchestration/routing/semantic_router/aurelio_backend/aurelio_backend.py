import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

# Create an embedding model
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials="<YOUR_OPENAI_API_KEY>"
)

# Pass em_invoker directly (auto-wrapped in v0.5+)
router = SemanticRouter.aurelio(
    encoder=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=valid_routes,
)
