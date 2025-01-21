import logging

from src.bridge.auxiliary_dataclasses import CandidateWithClusters
from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.external.metrics.factory import MetricsFactory
from src.external.metrics.storage import MetricsStorage
from src.logger.logging_config import frontend_manager
from src.measurement_storage.storage import MeasurementStorage
from src.moduslam.backend_manager.graph_solver import GraphSolver
from src.moduslam.data_manager.batch_factory.batch import DataBatch
from src.moduslam.frontend_manager.graph_builders.simple.graph_factory import (
    Factory as GraphFactory,
)
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.measurement_storage_analyzers.analyzers import (
    DoublePoseOdometry,
)
from src.moduslam.frontend_manager.utils import fill_storage
from src.utils.auxiliary_methods import nanosec2sec

logger = logging.getLogger(frontend_manager)


class Builder:
    """Builds sub-graph by connecting core measurements with IMU sequentially."""

    def __init__(self, handlers: set[Handler]):
        """
        Args:
            handlers: handlers for creating measurements.
        """
        self._handlers = handlers
        self._analyzer = DoublePoseOdometry()
        self._factory = GraphFactory()
        self._metrics_factory = MetricsFactory()
        self._metrics_storage = MetricsStorage()
        self._solver = GraphSolver()

    def create_graph(self, graph: Graph, data_batch: DataBatch) -> Graph:
        """Creates graph candidate using the measurements from the data batch.

        Args:
            graph: a main graph.

            data_batch: a data batch with elements.

        Returns:
            a new graph.
        """
        storage = MeasurementStorage

        while not data_batch.empty:

            fill_storage(storage, data_batch, self._handlers, self._analyzer)

            data = storage.data()
            can_with_clusters = self._factory.create_candidate_with_clusters(graph, data)
            graph = can_with_clusters.candidate.graph

            result_values, error = self._solver.solve(graph)
            graph.update_vertices(result_values)

            self._evaluate(can_with_clusters, error)

            storage.clear()

        logger.info("Input data batch is empty.")
        return graph

    def _evaluate(self, candidate_with_clusters: CandidateWithClusters, error: float) -> None:
        """Evaluates the candidate with clusters and stores the metrics.

        Args:
            candidate_with_clusters: a candidate with clusters.

            error: solver error.
        """
        candidate = candidate_with_clusters.candidate

        result = self._metrics_factory.evaluate(candidate_with_clusters, error)

        self._metrics_storage.add_unused_measurements(candidate, result.num_unused_measurements)
        self._metrics_storage.add_mom(candidate, result.mom)
        self._metrics_storage.add_connectivity(candidate, result.connectivity)
        self._metrics_storage.add_timeshift(candidate, result.timeshift)
        self._metrics_storage.add_solver_error(candidate, error)

        shift = self._metrics_storage.get_timeshift_table()[candidate]
        mom = self._metrics_storage.get_mom_table()[candidate]
        error = self._metrics_storage.get_error_table()[candidate]
        num_unused = candidate.num_unused_measurements

        secs_shift = nanosec2sec(shift)

        logger.debug(
            f"Best candidate: mom={mom}, error={error}, shift={secs_shift}, unused={num_unused}"
        )

        self._metrics_storage.clear()
