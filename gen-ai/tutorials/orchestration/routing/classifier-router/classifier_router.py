"""Classifier Router: pre-trained ML classifier routing (MLP, SVM).

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/classifier-router
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router.backend.llmrouter.config import MLPConfig, SVMConfig
from gllm_pipeline.router.classifier_router import ClassifierRouter

load_dotenv()

MODELS_DIR = Path(__file__).parent / "models"

QUERIES = [
    "What's 15% of 240?",
    "Write a detailed essay comparing the economic policies of three different countries.",
]


async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipped: set OPENAI_API_KEY to run router.route().")
        return

    encoder = build_em_invoker(
        model_id="openai/text-embedding-3-small",
        credentials=os.getenv("OPENAI_API_KEY"),
    )

    mlp_router = ClassifierRouter.mlp(
        model_path=str(MODELS_DIR / "mlp_model.pt"),
        default_route="gpt-5-nano-2025-08-07",
        valid_routes={"gpt-5-nano-2025-08-07", "gpt-5.4-2026-03-05"},
        config=MLPConfig(
            num_classes=2,
            input_dim=1536,
            idx_to_model={0: "gpt-5.4-2026-03-05", 1: "gpt-5-nano-2025-08-07"},
            hidden_layer_sizes=[128, 64],
            activation="relu",
        ),
        encoder=encoder,
    )

    svm_router = ClassifierRouter.svm(
        model_path=str(MODELS_DIR / "svm_model.pkl"),
        default_route="gpt-5-nano-2025-08-07",
        valid_routes={"gpt-5-nano-2025-08-07", "gpt-5.4-2026-03-05"},
        config=SVMConfig(num_classes=2),
        encoder=encoder,
    )

    for query in QUERIES:
        mlp_route = await mlp_router.route(query)
        svm_route = await svm_router.route(query)
        print(f"Query: {query}\nMLP route: {mlp_route}\nSVM route: {svm_route}\n")


if __name__ == "__main__":
    asyncio.run(main())
