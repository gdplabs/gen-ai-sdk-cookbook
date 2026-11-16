from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset


def main():
    """Main function."""
    raw_dataset = DictDataset.from_huggingface_hub(
        path_or_name="MathArena/hmmt_feb_2026",
        split="train",
    )
    data = [
        # Each row is an LLMTestCase; the dataset's own columns are extra fields.
        LLMTestCase(
            input=row.problem,
            actual_output=row.answer,
            expected_output=row.answer,
        )
        for row in raw_dataset.load()[:3]
    ]
    print(data)


if __name__ == "__main__":
    main()
