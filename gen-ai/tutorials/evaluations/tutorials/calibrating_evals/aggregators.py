from gllm_evals.types import EvaluatorResult, MetricInput


def _compute_rate(
    evaluation_results: list[list[EvaluatorResult]],
    data: list[MetricInput],
    evaluator_key: str,
    target_label: str,
    target_success: bool,
    metric_name: str,
) -> dict[str, float]:
    """Compute success rate for test cases matching a target label and success condition.

    Args:
        evaluation_results: Nested list of evaluator results, one per test case.
        data: Test case data with labels.
        evaluator_key: Evaluator name to extract results for.
        target_label: Label value to filter cases ("TRUE" or "FALSE").
        target_success: Expected aggregate_success value (True for pass, False for fail).
        metric_name: Key name for the returned dict.

    Returns:
        Dict with metric_name as key and rate (0.0-1.0) as value.
    """
    count = 0
    actual = 0
    for row_results, row_data in zip(evaluation_results, data, strict=True):
        evaluation_result = next(
            (result for result in row_results if evaluator_key in result), None
        )
        if evaluation_result is None:
            continue
        aggregate_success = evaluation_result[evaluator_key]["aggregate_success"]
        label = (
            row_data["label"]
            if isinstance(row_data, dict)
            else getattr(row_data, "label", None)
        )
        if label == target_label:
            actual += 1
            if aggregate_success == target_success:
                count += 1

    if actual == 0:
        return {metric_name: 0.0}
    return {metric_name: count / actual}


def _make_true_negative_rate(evaluator_key: str):
    """Factory for a run aggregator that computes true negative rate.

    Counts cases where label='FALSE' and the evaluator correctly predicted failure.

    Args:
        evaluator_key: Evaluator name to track in results.

    Returns:
        Aggregator function that accepts (evaluation_results, data) and returns TNR dict.
    """
    def true_negative_rate(
        evaluation_results: list[list[EvaluatorResult]], data: list[MetricInput]
    ) -> dict[str, float]:
        return _compute_rate(
            evaluation_results,
            data,
            evaluator_key,
            "FALSE",
            False,
            "true_negative_rate",
        )

    true_negative_rate.__name__ = f"true_negative_rate_{evaluator_key}"
    return true_negative_rate


def _make_true_positive_rate(evaluator_key: str):
    """Factory for a run aggregator that computes true positive rate.

    Counts cases where label='TRUE' and the evaluator correctly predicted success.

    Args:
        evaluator_key: Evaluator name to track in results.

    Returns:
        Aggregator function that accepts (evaluation_results, data) and returns TPR dict.
    """
    def true_positive_rate(
        evaluation_results: list[list[EvaluatorResult]], data: list[MetricInput]
    ) -> dict[str, float]:
        return _compute_rate(
            evaluation_results, data, evaluator_key, "TRUE", True, "true_positive_rate"
        )

    true_positive_rate.__name__ = f"true_positive_rate_{evaluator_key}"
    return true_positive_rate


def compute_combined_metrics(
    results_with_keys: list[tuple[dict, str]],
) -> dict[str, float]:
    """Aggregate TPR and TNR across multiple evaluate() runs with different evaluators.

    Combines results from multiple evaluations (e.g., different evaluator categories)
    into a single combined TPR and TNR across all results.

    Args:
        results_with_keys: List of (results_dict, evaluator_key) tuples where
            results_dict is the output from evaluate().

    Returns:
        Dict with 'combined_tpr' and 'combined_tnr' keys and rates (0.0-1.0) as values.
    """
    tp = tn = actual_pos = actual_neg = 0
    for results, key in results_with_keys:
        for row in results["results"]:
            eval_result = next((r for r in row if key in r), None)
            if eval_result is None:
                continue
            label = eval_result.get("label")
            success = eval_result[key]["aggregate_success"]
            if label == "TRUE":
                actual_pos += 1
                if success:
                    tp += 1
            elif label == "FALSE":
                actual_neg += 1
                if not success:
                    tn += 1
    return {
        "combined_tpr": tp / actual_pos if actual_pos else 0.0,
        "combined_tnr": tn / actual_neg if actual_neg else 0.0,
    }
