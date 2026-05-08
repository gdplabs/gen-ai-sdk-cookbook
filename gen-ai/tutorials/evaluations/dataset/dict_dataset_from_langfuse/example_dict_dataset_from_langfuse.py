"""Example of loading a dataset from Langfuse using DictDataset (read-only).

Langfuse stores dataset item inputs as structured objects (dicts), so the
"input" field may be a dict rather than a plain string. Extract the relevant
key that matches your dataset schema (e.g. "query") before passing to LLMTestCase.

Authors:
    Mikhael Chris (mikhael.chris@gdplabs.id)

References:
    NONE
"""

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
            input=row["input"]["query"],
            actual_output=row["input"]["generated_response"],
            expected_output=row.get("expected_output"),
        )
        for row in raw_dataset.load()
    ]

    print(data)


if __name__ == "__main__":
    main()
