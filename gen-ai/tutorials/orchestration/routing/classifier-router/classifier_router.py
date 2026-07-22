"""Classifier Router — MLP and SVM backends.

The Classifier Router routes with a pre-trained ML classifier (MLP or SVM)
through the LLMRouter backend:

    from gllm_pipeline.router import ClassifierRouter
    from gllm_pipeline.router.backend.llmrouter.config import MLPConfig

    config = MLPConfig(
        num_classes=3,
        input_dim=768,
        idx_to_model={0: "billing", 1: "tech_support", 2: "faq"},
        hidden_layer_sizes=[256, 128],
        activation="relu",
        threshold=0.7,
    )
    router = ClassifierRouter.mlp(
        model_path="/path/to/mlp_model.pkl",
        default_route="faq",
        valid_routes={"billing", "tech_support", "faq"},
        config=config,
    )
    route = asyncio.run(router.route("How do I update my payment method?"))

Requirements: the ``llmrouter`` extra (``pip install "gllm-pipeline[llmrouter]"``)
— already declared in this directory's ``pyproject.toml``, which pulls in
PyTorch and scikit-learn.

This example is BLOCKED on a data artifact: it requires a pre-trained classifier
model file (``.pkl`` for sklearn / ``.pt`` for PyTorch) trained on your routing
labels. No such model ships with the SDK or this cookbook, so there is nothing
to point ``model_path`` at. Rather than fabricate a model, this script builds
the ``MLPConfig`` / ``SVMConfig`` (which validate offline) and then reports the
missing artifact.

Based on the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/classifier-router
"""

import os

from gllm_pipeline.router.backend.llmrouter.config import MLPConfig, SVMConfig

MLP_MODEL_PATH = "/path/to/mlp_model.pkl"
SVM_MODEL_PATH = "/path/to/svm_model.pkl"


def main() -> None:
    mlp_config = MLPConfig(
        num_classes=3,
        input_dim=768,
        idx_to_model={0: "billing", 1: "tech_support", 2: "faq"},
        hidden_layer_sizes=[256, 128],
        activation="relu",
        threshold=0.7,
    )
    svm_config = SVMConfig(num_classes=3, threshold=0.6)
    print(f"MLPConfig constructed: {mlp_config}")
    print(f"SVMConfig constructed: {svm_config}")

    if not os.path.exists(MLP_MODEL_PATH) and not os.path.exists(SVM_MODEL_PATH):
        print(
            "BLOCKED: no pre-trained classifier model available.\n"
            f"  Expected an MLP model at: {MLP_MODEL_PATH}\n"
            f"  or an SVM model at:       {SVM_MODEL_PATH}\n"
            "  Train an MLP/SVM classifier on your routing labels, then use\n"
            "  ClassifierRouter.mlp(...) / ClassifierRouter.svm(...) with the\n"
            "  resulting model file. See the GitBook page for full usage."
        )
        return

    import asyncio

    from gllm_pipeline.router import ClassifierRouter

    router = ClassifierRouter.mlp(
        model_path=MLP_MODEL_PATH,
        default_route="faq",
        valid_routes={"billing", "tech_support", "faq"},
        config=mlp_config,
    )
    route = asyncio.run(router.route("How do I update my payment method?"))
    print(f"Selected route: {route}")


if __name__ == "__main__":
    main()
