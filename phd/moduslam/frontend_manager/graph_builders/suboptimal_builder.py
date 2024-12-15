import logging

from phd.bridge.optimal_candidate_factory import Factory
from phd.external.handlers_factory.handlers.handler_protocol import Handler
from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.storage import MeasurementStorage
from phd.moduslam.data_manager.batch_factory.batch import DataBatch
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.measurement_storage_analyzers.analyzers import (
    DoublePoseOdometry,
)
from phd.moduslam.frontend_manager.utils import fill_storage

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
        self._storage = MeasurementStorage()

    def create_graph(self, graph: Graph, data_batch: DataBatch) -> Graph:
        """Creates graph candidate using the measurements from the data batch.

        Args:
            graph: a main graph.

            data_batch: a data batch with elements.

        Returns:
            a new graph.
        """
        new_graph = graph
        while not data_batch.empty:

            fill_storage(self._storage, data_batch, self._handlers, self._analyzer)

            candidate = self._candidate_factory.create_candidate(new_graph, self._storage)

            self._storage.clear()

            if candidate.leftovers:
                for measurement in candidate.leftovers:
                    self._storage.add(measurement)

            new_graph = candidate.graph

        logger.info("Input data batch is empty.")
        return new_graph
