from typing import Any

from phd.bridge.candidates_factory import Factory as CandidatesFactory
from phd.external.metrics.candidate_evaluator import Evaluator
from phd.measurements.measurement_storage import MeasurementStorage
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphCandidate


class Factory:
    """Creates suboptimal graph candidate."""

    def __init__(self):
        self._evaluator = Evaluator()
        self._factory = CandidatesFactory

    @property
    def is_ready(self) -> bool:
        """Checks if the candidate is ready for processing."""
        raise NotImplementedError

    def create_best_candidate(
        self, graph: Graph, measurements_storage: MeasurementStorage
    ) -> GraphCandidate:
        """Creates the best candidate.

        Args:
            graph: a main graph.

            measurements_storage: a storage with measurements.

        Returns:
            the best candidate.
        """
        results: dict[GraphCandidate, Any] = {}
        candidates = self._factory.create_candidates(graph, measurements_storage)

        for candidate in candidates:
            self._solve(candidate)
            result = self._evaluator.compute_metrics(candidate)
            results[candidate] = result

        best_candidate = self._choose_best(results)
        return best_candidate

    def _solve(self, candidate: GraphCandidate) -> None:
        """Solves the graph candidate."""
        raise NotImplementedError

    def _choose_best(self, candidates_with_metrics: dict[GraphCandidate, Any]) -> GraphCandidate:
        """Chooses the best candidate."""
        raise NotImplementedError
