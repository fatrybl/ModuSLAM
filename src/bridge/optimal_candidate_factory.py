# from src.bridge.candidates_factory_no_copy import Factory as CandidatesFactory
import logging
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.bridge.auxiliary_dataclasses import CandidateWithClusters
from src.bridge.candidates_factory import create_candidates_with_clusters
from src.external.metrics.factory import MetricsFactory, MetricsResult
from src.external.metrics.storage import MetricsStorage
from src.logger.logging_config import frontend_manager
from src.measurement_storage.measurements.base import Measurement
from src.moduslam.backend_manager.graph_solver import GraphSolver
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphCandidate
from src.utils.auxiliary_methods import nanosec2sec
from src.utils.exceptions import ItemNotExistsError
from src.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class Factory:
    """Creates suboptimal graph candidate."""

    def __init__(self):
        self._metrics_factory = MetricsFactory()
        self._metrics_storage = MetricsStorage()
        self._solver = GraphSolver()

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
        candidates_with_clusters = create_candidates_with_clusters(graph, data)
        self._evaluate(candidates_with_clusters)
        best_candidate = self._choose_best_candidate(self._metrics_storage)

        shift = self._metrics_storage.get_timeshift_table()[best_candidate]
        mom = self._metrics_storage.get_mom_table()[best_candidate]
        error = self._metrics_storage.get_error_table()[best_candidate]
        num_unused = best_candidate.num_unused_measurements

        secs_shift = nanosec2sec(shift)

        logger.debug(
            f"Best candidate: mom={mom}, error={error}, shift={secs_shift}, unused={num_unused}"
        )

        self._metrics_storage.clear()

        return best_candidate

    @staticmethod
    def _choose_best_candidate(storage: MetricsStorage) -> GraphCandidate:
        """Chooses the best candidate based on metrics in the storage.

        Args:
            storage: a storage with metrics.

        Returns:
            the best candidate.

        Raises:
            ItemNotExistsError: if no best candidate exists.
        """
        table = storage.get_timeshift_table()
        candidates = sorted(table, key=lambda k: table[k])
        for candidate in candidates:
            connectivity = storage.get_connectivity_status(candidate)
            if connectivity:
                return candidate

        raise ItemNotExistsError("No best candidate exists.")

    def _evaluate(self, items: Iterable[CandidateWithClusters]) -> None:
        """Evaluates candidates.

        Args:
            items: graph candidates with measurement clusters.
        """

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._evaluate_item, item): item for item in items}
            for future in as_completed(futures):
                candidate, result = future.result()
                self._metrics_storage.add_solver_error(candidate, result.solver_error)
                self._metrics_storage.add_num_unsued(candidate, result.num_unused_measurements)
                self._metrics_storage.add_connectivity(candidate, result.connectivity)
                self._metrics_storage.add_timeshift(candidate, result.timeshift)

        for item in items:
            candidate = item.candidate
            # mom = self._metrics_factory.compute_mom(candidate)
            mom = 0
            self._metrics_storage.add_mom(candidate, mom)

    def _evaluate_item(self, item: CandidateWithClusters) -> tuple[GraphCandidate, MetricsResult]:
        """Solves the graph, updates vertices and computes metrics (except MOM).

        Args:
            item: a graph candidate with clusters to solve and evaluate.

        Returns:
            candidate and metrics result.
        """

        candidate = item.candidate
        graph = item.candidate.graph
        values, error = self._solver.solve(graph)
        graph.update_vertices(values)

        connectivity = self._metrics_factory.compute_connectivity(candidate)
        timeshift = self._metrics_factory.compute_timeshift(item.clusters)

        result = MetricsResult(error, connectivity, timeshift, candidate.num_unused_measurements)
        return candidate, result
