from langfuse import Langfuse, get_client

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset


def main():
    """Main function."""
    langfuse_client: Langfuse = get_client()

    raw_dataset = DictDataset.from_langfuse(
        langfuse_client=langfuse_client,
        dataset_name="simple_qa_dataset",
    )

    data = [
        LLMTestCase(
            # item.input in Langfuse is a dict — extract the field matching your schema
            input=row.input["query"],
            actual_output=row.input["generated_response"],
            expected_output=getattr(row, "expected_output", None),
        )
        for row in raw_dataset.load()
    ]

    print(data)


if __name__ == "__main__":
    main()
