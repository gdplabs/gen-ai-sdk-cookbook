import logging
from typing import Any

from gllm_evals.constant import ResultKeys
from gllm_evals.types import EvaluatorResult, LLMTestCase, MetricInput

logger = logging.getLogger(__name__)


def _get_label(row_data: MetricInput | LLMTestCase) -> bool | None:
    if hasattr(row_data, "label"):
        raw = row_data.label  # type: ignore[union-attr]
    else:
        raw = row_data.get("label")  # type: ignore[union-attr]

    if raw is None:
        return None
    if isinstance(raw, bool):
        return raw
    # Normalize string variants from CSV/Sheets ("TRUE", "true", "False", etc.)
    return str(raw).strip().upper() == "TRUE"


def _compute_binary_rate(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
    target_label: bool,
    target_success: bool,
    metric_key: str,
) -> dict[str, Any]:
    """Compute the fraction of matching predictions over rows with the given target_label.

    For each evaluator, counts rows where label == target_label and
    aggregate_success matches target_success, divided by total rows with
    that label where the evaluator produced a result.

    Args:
        evaluation_results: Accumulated row-grouped evaluation results.
        data: Accumulated input data, parallel to evaluation_results.
        target_label: Label value to filter rows on (``True`` for positive, ``False`` for negative).
        target_success: Expected aggregate_success value for a "correct" prediction.
        metric_key: Top-level key in the returned dict (e.g. ``"true_positive_rate"``).

    Returns:
        dict with metric_key mapping to per-evaluator rate values in ``[0.0, 1.0]``.
        Returns ``None`` when no rows with target_label exist in data.
        Returns 0.0 for an evaluator when rows with target_label exist but none produced a result.
    """
    if not evaluation_results:
        logger.warning(
            "%s: no evaluation results provided — returning empty rates.", metric_key
        )
        return {metric_key: {}}

    evaluator_names = {
        eval_name
        for row_results in evaluation_results
        for result in row_results
        for eval_name, eval_data in result.items()
        if isinstance(eval_data, dict) and ResultKeys.AGGREGATE_SUCCESS in eval_data
    }

    labels = [_get_label(d) for d in data]
    found_labels = set(labels)
    if target_label not in found_labels:
        logger.warning(
            "%s: no evaluator results found for label=%r. "
            "Labels present in data: %s. "
            "Check that the 'label' field is set on your test cases.",
            metric_key,
            target_label,
            found_labels,
        )
        return {metric_key: {eval_name: None for eval_name in evaluator_names}}

    rates = {}
    for eval_name in evaluator_names:
        matched = 0
        total = 0
        for row_results, label in zip(evaluation_results, labels, strict=True):
            if label != target_label:
                continue
            for result in row_results:
                eval_data = result.get(eval_name)
                if (
                    isinstance(eval_data, dict)
                    and ResultKeys.AGGREGATE_SUCCESS in eval_data
                ):
                    success = bool(eval_data[ResultKeys.AGGREGATE_SUCCESS])
                    matched += success == target_success
                    total += 1
                    break
        rates[eval_name] = round(matched / total, 2) if total else 0.0

    return {metric_key: rates}


def true_positive_rate(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, Any]:
    """Compute per-evaluator true positive rate (TPR) across data points.

    TPR measures how well an evaluator accepts responses that are labelled as
    correct (``"TRUE"``). Also known as sensitivity.

    Equation::

        TPR = TP / (TP + FN)

    where TP = label is ``"TRUE"``, evaluator ran, and ``aggregate_success`` is ``True``;
    FN = label is ``"TRUE"``, evaluator ran, and ``aggregate_success`` is ``False``.
    Rows where the evaluator did not produce a result are excluded from both
    numerator and denominator.

    Args:
        evaluation_results (list[list[EvaluatorResult]]): Accumulated
            row-grouped evaluation results.
        data (list[MetricInput]): Accumulated input data. Each item must
            have a ``label`` field with value ``"TRUE"`` or ``"FALSE"``.

    Returns:
        dict[str, Any]: Mapping with key ``"true_positive_rate"`` whose value
        is a dict of per-evaluator TPR values in ``[0.0, 1.0]``.
    """
    return _compute_binary_rate(
        evaluation_results,
        data,
        target_label=True,
        target_success=True,
        metric_key="true_positive_rate",
    )


def true_negative_rate(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
) -> dict[str, Any]:
    """Compute per-evaluator true negative rate (TNR) across data points.

    TNR measures how well an evaluator rejects responses that are labelled as
    incorrect (``"FALSE"``). Also known as specificity.

    Equation::

        TNR = TN / (TN + FP)

    where TN = label is ``"FALSE"``, evaluator ran, and ``aggregate_success`` is ``False``;
    FP = label is ``"FALSE"``, evaluator ran, and ``aggregate_success`` is ``True``.
    Rows where the evaluator did not produce a result are excluded from both
    numerator and denominator.

    Args:
        evaluation_results (list[list[EvaluatorResult]]): Accumulated
            row-grouped evaluation results.
        data (list[MetricInput]): Accumulated input data. Each item must
            have a ``label`` field with value ``"TRUE"`` or ``"FALSE"``.

    Returns:
        dict[str, Any]: Mapping with key ``"true_negative_rate"`` whose value
        is a dict of per-evaluator TNR values in ``[0.0, 1.0]``.
    """
    return _compute_binary_rate(
        evaluation_results,
        data,
        target_label=False,
        target_success=False,
        metric_key="true_negative_rate",
    )


def compute_combined_metrics(
    results_with_keys: list[tuple[dict, str, list[MetricInput]]],
) -> dict[str, float | None]:
    """Aggregate TPR and TNR across multiple evaluate() runs with different evaluators.

    Combines results from multiple evaluations (e.g., different evaluator categories)
    into a single combined TPR and TNR across all results.

    Args:
        results_with_keys: List of (results_dict, evaluator_key, data) tuples where
            results_dict is the output from evaluate() and data is the original input
            list used for that evaluation run.

    Returns:
        Dict with 'combined_tpr' and 'combined_tnr' keys and rates (0.0-1.0) as values.
    """
    tp = tn = actual_pos = actual_neg = 0
    for results, key, data in results_with_keys:
        for row, row_data in zip(results["results"], data, strict=True):
            eval_result = next((r for r in row if key in r), None)
            if eval_result is None:
                continue
            label = _get_label(row_data)
            success = eval_result[key][ResultKeys.AGGREGATE_SUCCESS]
            if label is True:
                actual_pos += 1
                if success:
                    tp += 1
            elif label is False:
                actual_neg += 1
                if not success:
                    tn += 1
    return {
        "combined_tpr": tp / actual_pos if actual_pos else None,
        "combined_tnr": tn / actual_neg if actual_neg else None,
    }
