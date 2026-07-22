"""Semantic Router — KNN backend.

Uses ``SemanticRouter.knn()`` with a pre-trained KNeighborsClassifier model for
lightweight, classification-based routing:

    from gllm_pipeline.router.backend.llmrouter.config import KNNConfig

    router = SemanticRouter.knn(
        default_route="faq",
        valid_routes={"billing", "tech_support", "faq"},
        model_path="/path/to/knn_model.pkl",
        config=KNNConfig(num_classes=3),
    )
    route = asyncio.run(router.route("How do I update my payment method?"))

Requirements: the ``llmrouter`` extra (``pip install "gllm-pipeline[llmrouter]"``)
— already declared in this directory's ``pyproject.toml``.

This example is BLOCKED on a data artifact: it requires a pre-trained KNN
classifier model file (``knn_model.pkl``) trained on your routing labels. No
such model ships with the SDK or this cookbook, so there is nothing to point
``model_path`` at. Rather than fabricate a model, this script constructs the
``KNNConfig`` (which validates offline) and then reports the missing artifact.

Based on the "Option 4: KNN Backend" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router
"""

import os

from gllm_pipeline.router.backend.llmrouter.config import KNNConfig

MODEL_PATH = "/path/to/knn_model.pkl"


def main() -> None:
    config = KNNConfig(num_classes=3)
    print(f"KNNConfig constructed: {config}")

    if not os.path.exists(MODEL_PATH):
        print(
            "BLOCKED: no pre-trained KNN model available.\n"
            f"  Expected a trained KNeighborsClassifier at: {MODEL_PATH}\n"
            "  Train a KNN classifier on your routing labels and point\n"
            "  `model_path` at the resulting .pkl to enable this backend.\n"
            "  See the GitBook page for the full SemanticRouter.knn(...) usage."
        )
        return

    # Reached only when a real model is supplied (not the case in CI/offline).
    import asyncio

    from gllm_pipeline.router import SemanticRouter

    router = SemanticRouter.knn(
        default_route="faq",
        valid_routes={"billing", "tech_support", "faq"},
        model_path=MODEL_PATH,
        config=config,
    )
    route = asyncio.run(router.route("How do I update my payment method?"))
    print(f"Selected route: {route}")


if __name__ == "__main__":
    main()
