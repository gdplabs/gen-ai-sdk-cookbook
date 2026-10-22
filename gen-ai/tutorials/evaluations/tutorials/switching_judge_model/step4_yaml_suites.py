"""Step 4: Switch the model from YAML.

Loads every suite in suites/ with EvalSuite.from_yaml_dir(). The model comes from the
JUDGE_MODEL env var and defaults to openai/gpt-6-luna.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites

load_dotenv()


async def main():
    suites = EvalSuite.from_yaml_dir("suites")
    result = await evaluate_suites(suites=suites)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
