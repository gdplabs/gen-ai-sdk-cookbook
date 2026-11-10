import asyncio

from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.utils.demo_utils import your_ai_func_result


async def main():
    """Main function."""
    # Map the CSV columns to LLMTestCase fields.
    dataset = DictDataset.from_csv(
        "examples/simple_qa_data.csv",
        field_mapping={"query": "input", "expected_response": "expected_output"},
    )

    # Add the output of your AI system to each row.
    data = []
    for row in dataset.load():
        ai_result = your_ai_func_result(row.input)
        data.append(
            row.model_copy(
                update={
                    "actual_output": ai_result["actual output"],
                    "retrieved_context": ai_result["retrieved_context"],
                }
            )
        )

    print(data)


if __name__ == "__main__":
    asyncio.run(main())
