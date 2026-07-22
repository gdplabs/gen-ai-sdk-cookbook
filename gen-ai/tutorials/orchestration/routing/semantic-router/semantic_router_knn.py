"""Semantic Router: KNN backend using a pretrained classifier model.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#option-4-knn-backend

Requirements:
    pip install "gllm-pipeline[llmrouter]"
"""
from __future__ import annotations

import asyncio

from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.backend.llmrouter.config import KNNConfig


def main() -> None:
    router = SemanticRouter.knn(
        default_route="faq",
        valid_routes={"billing", "tech_support", "faq"},
        model_path="/path/to/knn_model.pkl",
        config=KNNConfig(num_classes=3),
    )

    query = "My subscription payment failed and invoices are missing"
    route = asyncio.run(router.route(query))
    print(f"Selected route: {route}")


if __name__ == "__main__":
    main()
