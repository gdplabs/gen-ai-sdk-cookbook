"""Semantic Router — using presets (`from_preset`).

The GitBook page shows loading a predefined route configuration:

    from gllm_pipeline.router.schema import BackendType, ModalityType

    router = SemanticRouter.from_preset(
        backend=BackendType.AURELIO,
        preset_name="customer_support",
        modality=ModalityType.TEXT,
        default_route="general",
        valid_routes={"billing", "tech_support", "general"},
    )

Heads-up on the installed version: the only preset bundled with the Aurelio
backend is ``(ModalityType.IMAGE, "domain_specific")`` — an image-classification
preset that requires a live multimodal embedding model (real credentials). The
text ``customer_support`` preset shown in the GitBook is not shipped in this
release. Calling ``from_preset`` for an unbundled combination raises a
``ValueError`` that lists the supported combinations.

To keep this example runnable offline, it introspects and prints the presets
actually bundled in the installed ``gllm-pipeline`` rather than making a live
model call. For a runnable routing demo, see ``native_backend.py`` /
``aurelio_em_invoker.py``, which pass explicit ``route_examples``.

Based on the "Using Presets" section of the GitBook page:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router
"""

from gllm_pipeline.router.backend.aurelio.aurelio_adapter import (
    AURELIO_PRESET_MAPPING,
)


def main() -> None:
    print("Bundled Aurelio presets in the installed gllm-pipeline:\n")
    for (modality, preset_name), routes in AURELIO_PRESET_MAPPING.items():
        print(f"- modality={modality.value!r}, preset_name={preset_name!r}")
        print(f"  routes: {sorted(routes.keys())}\n")


if __name__ == "__main__":
    main()
