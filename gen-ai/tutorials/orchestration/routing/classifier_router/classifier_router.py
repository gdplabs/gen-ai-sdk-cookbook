import asyncio
from gllm_pipeline.router import ClassifierRouter
from gllm_pipeline.router.backend.llmrouter.config import MLPConfig

# Configure the MLP classifier
config = MLPConfig(
    num_classes=3,
    input_dim=768,
    idx_to_model={0: "billing", 1: "tech_support", 2: "faq"},
    hidden_layer_sizes=[256, 128],
    activation="relu",
    threshold=0.7,  # Confidence threshold; 0.0 disables it
)

# Create the router
router = ClassifierRouter.mlp(
    model_path="/path/to/mlp_model.pkl",
    default_route="faq",
    valid_routes={"billing", "tech_support", "faq"},
    config=config,
)

# Route a query
route = asyncio.run(router.route("How do I update my payment method?"))
print(f"Selected route: {route}")  # Output: "billing"
