from phd.bridge.candidates_factory import Factory as CandidatesFactory
from phd.external.metrics.storage import MetricsStorage
from phd.external.metrics.vertices_connectivity import VerticesConnectivity
from phd.measurement_storage.storage import MeasurementStorage
from phd.moduslam.backend_manager.graph_solver import GraphSolver
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphCandidate
from phd.moduslam.utils.exceptions import ItemNotExistsError


class Factory:
    """Creates suboptimal graph candidate."""

    def __init__(self):
        self._solver = GraphSolver()
        self._factory = CandidatesFactory

    @property
    def is_ready(self) -> bool:
        """Checks if the candidate is ready for processing."""
        raise NotImplementedError

    def create_candidate(
        self, graph: Graph, measurements_storage: MeasurementStorage
    ) -> GraphCandidate:
        """Creates the best candidate.

        Args:
            graph: a main graph.

            measurements_storage: a storage with measurements.

        Returns:
            the best candidate.
        """
        candidates = self._factory.create_candidates(graph, measurements_storage)

        for candidate in candidates:
            error = self._solve(candidate.graph)
            connectivity = VerticesConnectivity.compute(candidate.graph, candidate.elements)

            MetricsStorage.add_error(candidate, error)
            MetricsStorage.add_connectivity(candidate, connectivity)

        best_candidate = self._choose_best()
        return best_candidate

    def _solve(self, graph: Graph) -> float:
        """Solves and updates the graph."""
        values, error = self._solver.solve(graph)
        graph.update_vertices(values)
        return error

    @staticmethod
    def _choose_best() -> GraphCandidate:
        """Chooses the best candidate.

        Raises:
            ItemNotExistsError: if no best candidate exists.
        """
        table = MetricsStorage.get_timeshift_table()
        candidates = sorted(table, key=lambda k: table[k])
        for candidate in candidates:
            connectivity = MetricsStorage.get_connectivity_status(candidate)
            if connectivity:
                return candidate

        raise ItemNotExistsError("No best candidate exists.")
