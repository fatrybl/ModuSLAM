import numpy as np

from phd.moduslam.frontend_manager.main_graph.objects import GraphCandidate


class Evaluator:

    @staticmethod
    def compute_metrics(candidate: GraphCandidate):
        raise NotImplementedError


def evaluate(items: list, metrics: list, weights: np.ndarray):
    """Evaluates each item with every metric and weights.

    Args:
        items: items to be evaluated.

        metrics: different metrics to evaluate.

        weights: weights for metrics summarization.

    Returns:
        scores, best score, item index with the best score.
    """
    scores = []
    best_value = float("-inf")
    best_item_idx = -1

    for idx, item in enumerate(items):
        metric_values = [metric.compute(item) for metric in metrics]
        score = metric_values @ weights.T
        scores.append(score)

        if score > best_value:
            best_value = score
            best_item_idx = idx

    return scores, best_value, best_item_idx
