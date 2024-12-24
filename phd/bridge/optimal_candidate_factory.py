from phd.bridge.candidates_factory_no_copy import Factory as CandidatesFactory
from phd.external.metrics.storage import MetricsStorage
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphCandidate
from phd.utils.exceptions import ItemNotExistsError
from phd.utils.ordered_set import OrderedSet


class Factory:
    """Creates suboptimal graph candidate."""

    def __init__(self):
        self._factory = CandidatesFactory()

    @property
    def is_ready(self) -> bool:
        """Checks if the candidate is ready for processing."""
        raise NotImplementedError

    def create_candidate(
        self, graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> GraphCandidate:
        """Creates the best candidate.

        Args:
            graph: a main graph.

            data: a table of measurements grouped by type.

        Returns:
            the best candidate.
        """
        _ = self._factory.create_candidates(graph, data)
        best_candidate = self._choose_best()
        return best_candidate

    @staticmethod
    def _choose_best() -> GraphCandidate:
        """Chooses the best candidate.

        Raises:
            ItemNotExistsError: if no best candidate exists.
        """
        table = MetricsStorage.get_mom_table()
        candidates = sorted(table, key=lambda k: table[k])
        for candidate in candidates:
            connectivity = MetricsStorage.get_connectivity_status(candidate)
            if connectivity:
                MetricsStorage.clear()
                return candidate

        raise ItemNotExistsError("No best candidate exists.")
