"""Filtering log records with LoggerManager.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#filtering-log-records
"""

import logging

from gllm_core.logging import LoggerManager


def main() -> None:
    """Register a logger-name filter on the manager's handlers."""
    manager = LoggerManager()
    manager.add_filter(logging.Filter("my_application"))


if __name__ == "__main__":
    main()
