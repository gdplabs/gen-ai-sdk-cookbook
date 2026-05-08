"""Example of using the LangfuseExperimentTracker to refresh or export langfuse session-level score.

Authors:
    Christina Alexandra (christina.alexandra@gdplabs.id)

References:
    NONE
"""

import asyncio
import datetime as dt

from langfuse import get_client

from gllm_evals.experiment_tracker.langfuse_experiment_tracker import (
    LangfuseExperimentTracker,
)
from gllm_evals.utils.langfuse_manager import LangfuseTracesSearchParams


async def main():
    """The main function to run refresh or export langfuse session-level score."""
    run_id = ""  # Fill this with the session id you want to refresh
    exp_tracker = LangfuseExperimentTracker(
        langfuse_client=get_client(),
        project_name="glchat_beta",
    )

    # 1. Refresh score
    exp_tracker.refresh_score(
        run_id=run_id,
        search_params={
            LangfuseTracesSearchParams.FROM_TIMESTAMP: dt.datetime.now()
            - dt.timedelta(days=6),
            LangfuseTracesSearchParams.TO_TIMESTAMP: dt.datetime.now(),
        },
    )

    # 2. Export experiment results
    exp_tracker.export_experiment_results(
        run_id=run_id,
        search_params={"limit": 100},
    )


if __name__ == "__main__":
    asyncio.run(main())
