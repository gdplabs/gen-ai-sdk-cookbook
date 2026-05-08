"""Example of using the evaluate convenience function with a dataset loader.

The simple QA CSV uses domain-specific column names. This example shows how to
remap them to the canonical field names expected by evaluators before evaluation.

Authors:
    Christina Alexandra (christina.alexandra@gdplabs.id)
    Mikhael Chris (mikhael.chris@gdplabs.id)

References:
    NONE
"""

import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.utils.demo_utils import your_ai_func_result


async def main():
    """Main function."""
    data = [  # noqa: F841
        LLMTestCase(
            input=row["query"],
            actual_output=your_ai_func_result(row["query"])["actual output"],
            expected_output=row["expected_response"],
            retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
        )
        for row in DictDataset.from_csv("examples/sample_data/simple_qa_data.csv").load()
    ]


if __name__ == "__main__":
    asyncio.run(main())
