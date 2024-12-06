from typing import Any

from phd.bridge.candidates_factory import Factory as CandidatesFactory
from phd.external.metrics.candidate_evaluator import Evaluator
from phd.measurements.storage import MeasurementStorage
from phd.moduslam.backend_manager.graph_solver import GraphSolver
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphCandidate
from phd.moduslam.map_manager.graph_saver import GraphSaver


class Factory:
    """Creates suboptimal graph candidate."""

    def __init__(self):
        self._evaluator = Evaluator()
        self._solver = GraphSolver()
        self._factory = CandidatesFactory
        self._graph_saver = GraphSaver()

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
        results: list[tuple[GraphCandidate, Any]] = []
        candidates = self._factory.create_candidates(graph, measurements_storage)

        for i, candidate in enumerate(candidates):
            self._solve(candidate.graph, i)
            results.append((candidate, None))

        best_candidate = self._choose_best(results)
        return best_candidate

    def _solve(self, graph: Graph, index: int) -> None:
        """Solves and updates the graph."""
        values = self._solver.solve(graph)
        print(f"VARIANT {index}: {values}")
        graph.update_vertices(values)
        self._graph_saver.save_to_pdf(graph, name=str(index))

    @staticmethod
    def _choose_best(candidates_with_metrics: list[tuple[GraphCandidate, Any]]) -> GraphCandidate:
        """Chooses the best candidate."""
        return candidates_with_metrics[0][0]
