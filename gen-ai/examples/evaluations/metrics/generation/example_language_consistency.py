import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.generation.language_consistency import LanguageConsistencyMetric
from gllm_evals.types import RAGData


async def main() -> None:
    """Run a simple Language Consistency evaluation example."""
    dataset = [
        RAGData(  # Good case (response language matches query language)
            query="¿Cómo puedo restablecer mi contraseña?",
            generated_response="Puede restablecer su contraseña haciendo clic en el enlace 'Olvidé mi contraseña' en la página de inicio de sesión.",
        ),
        RAGData(  # Bad case (response language differs from query language)
            query="¿Cómo puedo restablecer mi contraseña?",
            generated_response="You can reset your password by clicking on the 'Forgot Password' link on the login page.",
        ),
    ]

    # Initialize the metric
    metric = LanguageConsistencyMetric(
        model=DefaultValues.MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        use_reasoning=True,
    )

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        print("Score:", result["language_consistency"]["score"])
        print("Reason:", result["language_consistency"]["explanation"], "\n")


if __name__ == "__main__":
    asyncio.run(main())
