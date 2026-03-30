"""Metric tracking mixin for automatic pytest result collection.

Provides MetricTrackingMixin that can be inherited by evaluator classes
to automatically track and inject metric results into pytest nodes.

Author:
    - Mikhael Chris (mikhael.chris@gdplabs.id)
"""

from typing import Any, Optional


class MetricTrackingMixin:
    """Mixin that adds automatic metric tracking to evaluator classes.

    This mixin provides a `_track` method that captures metric results
    and injects them into pytest nodes for result collection.

    Classes using this mixin must call `_init_tracking(request)` in their __init__
    if they want to enable tracking.
    """

    def _init_tracking(self, request: Optional[Any] = None) -> None:
        """Initialize tracking state.

        Args:
            request: Optional pytest request fixture for accessing test node.
                    If None, tracking is disabled.
        """
        self._request = request
        self._metrics: dict[str, Any] = {}

    def _track(self, metric_name: str, value: Any) -> Any:
        """Track a metric value and inject into pytest node if tracking is enabled.

        Args:
            metric_name: Name of the metric being tracked.
            value: Metric result value.

        Returns:
            The same value that was passed in.
        """
        if hasattr(self, "_request") and self._request is not None:
            self._metrics[metric_name] = value
            if hasattr(self._request, "node"):
                self._request.node.metric_data = self._metrics.copy()
        return value
