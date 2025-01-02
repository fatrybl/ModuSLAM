# from phd.bridge.candidates_factory_no_copy import Factory as CandidatesFactory
from collections.abc import Iterable

from phd.bridge.auxiliary_dataclasses import CandidateWithClusters
from phd.bridge.candidates_factory import Factory as CandidatesFactory
from phd.external.metrics.factory import MetricsFactory
from phd.external.metrics.storage import MetricsStorage
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphCandidate
from phd.utils.exceptions import ItemNotExistsError
from phd.utils.ordered_set import OrderedSet


class Factory:
    """Creates suboptimal graph candidate."""

    def __init__(self):
        self._candidates_factory = CandidatesFactory()
        self._metrics_factory = MetricsFactory()
        self._metrics_storage = MetricsStorage()

    def create_candidate(
        self, graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> GraphCandidate:
        """Creates optimal graph candidate.

        Args:
            graph: a main graph.

            data: a table of measurements grouped by type.

        Returns:
            optimal candidate.
        """
        candidates_with_clusters = self._candidates_factory.create_candidates(graph, data)
        self._evaluate(candidates_with_clusters)
        best_candidate = self._choose_best(self._metrics_storage)

        shift = self._metrics_storage.get_timeshift_table()[best_candidate]
        mom = self._metrics_storage.get_mom_table()[best_candidate]
        error = self._metrics_storage.get_error_table()[best_candidate]

        print(f"Best candidate metrics: mom={mom}, error={error}, shift={shift}\n")

        self._metrics_storage.clear()

        return best_candidate

    def _evaluate(self, items: Iterable[CandidateWithClusters]) -> None:
        """Evaluates candidates.

        Args:
            items: graph candidates with measurement clusters.
        """

        for item in items:
            can = item.candidate

            result = self._metrics_factory.evaluate(item)

            self._metrics_storage.add_mom(can, result.mom)
            self._metrics_storage.add_connectivity(can, result.connectivity)
            self._metrics_storage.add_timeshift(can, result.timeshift)
            self._metrics_storage.add_solver_error(can, result.solver_error)

    @staticmethod
    def _choose_best(storage: MetricsStorage) -> GraphCandidate:
        """Chooses the best candidate.

        Args:
            storage: a storage with metrics.

        Raises:
            ItemNotExistsError: if no best candidate exists.
        """
        table = storage.get_mom_table()
        candidates = sorted(table, key=lambda k: table[k])
        for candidate in candidates:
            connectivity = storage.get_connectivity_status(candidate)
            if connectivity:
                return candidate

        raise ItemNotExistsError("No best candidate exists.")
