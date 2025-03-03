import logging

from src.bridge.optimal_candidate_factory import Factory
from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.external.metrics.factory import MetricsResult
from src.logger.logging_config import frontend_manager
from src.measurement_storage.storage import MeasurementStorage
from src.moduslam.data_manager.batch_factory.batch import DataBatch
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.measurement_storage_analyzers.analyzers import (
    DoublePoseOdometry,
)
from src.moduslam.frontend_manager.utils import fill_storage
from src.utils.auxiliary_methods import nanosec2sec

logger = logging.getLogger(frontend_manager)


class Builder:
    """Creates multiple edges combinations and chooses the best one."""

    def __init__(self, handlers: set[Handler]):
        """
        Args:
            handlers: handlers for creating measurements.
        """
        self._handlers = handlers
        self._analyzer = DoublePoseOdometry()
        self._candidate_factory = Factory()

    def create_graph(self, graph: Graph, data_batch: DataBatch) -> Graph:
        """Creates graph candidate using the measurements from the data batch.

        Args:
            graph: a main graph.

            data_batch: a data batch with elements.

        Returns:
            a new graph.
        """
        storage = MeasurementStorage

        total_metrics = MetricsResult()

        while not data_batch.empty:

            fill_storage(storage, data_batch, self._handlers, self._analyzer)

            data = storage.data()
            candidate, new_metrics = self._candidate_factory.create_candidate(graph, data)

            accumulate_metrics(total_metrics, new_metrics)

            storage.clear()

            if candidate.leftovers:
                logger.warning("Adding leftovers back to storage")
                for measurement in candidate.leftovers:
                    storage.add(measurement)

            graph = candidate.graph

        logger.info("Input data batch is empty.")
        print_metrics(total_metrics)
        return graph


def accumulate_metrics(existing: MetricsResult, new: MetricsResult):
    """Accumulates metrics.

    Args:
        existing: existing metrics.

        new: new metrics.

    Returns:
        accumulated metrics.
    """
    existing.solver_error = new.solver_error
    existing.connectivity = new.connectivity
    existing.timeshift += new.timeshift
    existing.num_unused_measurements += new.num_unused_measurements
    existing.mom += new.mom


def print_metrics(metrics: MetricsResult):
    """Prints metrics.

    Args:
        metrics: metrics to print.
    """
    logger.info(f"Solver error: {metrics.solver_error}")
    logger.info(f"Connectivity: {metrics.connectivity}")
    logger.info(f"Timeshift: {nanosec2sec(metrics.timeshift)}")
    logger.info(f"Unused measurements: {metrics.num_unused_measurements}")
    logger.info(f"MOM: {metrics.mom}")
