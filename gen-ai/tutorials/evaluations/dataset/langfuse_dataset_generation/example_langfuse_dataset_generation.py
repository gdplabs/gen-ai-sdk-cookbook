import asyncio

from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.dataset.langfuse_dataset import LangfuseDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from langfuse import Langfuse, get_client


async def main():
    """Main function."""
    langfuse_client: Langfuse = get_client()

    langfuse_dataset = LangfuseDataset.from_dict(
        dataset=DictDataset.from_csv("examples/sample_data/simple_qa_data.csv"),
        langfuse_client=langfuse_client,
        dataset_name="simple_qa_dataset",
    )
    dataset = langfuse_dataset.dataset

    evaluator = GEvalGenerationEvaluator()

    # Convert to LLMTestCase format
    data = [
        LLMTestCase(
            input=row.get("query"),
            actual_output=row.get("generated_response"),
            expected_output=row.get("expected_response"),
            retrieved_context=row.get("retrieved_context"),
        )
        for row in dataset
    ]

    suite = EvalSuite(
        data=data,
        evaluators=[evaluator],
    )
    results = await evaluate_suites(
        suites=[suite],
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
