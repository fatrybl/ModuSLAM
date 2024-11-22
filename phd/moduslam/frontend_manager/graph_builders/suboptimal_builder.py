import logging

from phd.bridge.optimal_candidate_factory import Factory
from phd.logger.logging_config import frontend_manager
from phd.measurements.measurement_storage import MeasurementStorage
from phd.moduslam.data_manager.batch_factory.batch import DataBatch
from phd.moduslam.frontend_manager.handlers.handler_protocol import Handler
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.measurement_storage_analyzers.analyzers import (
    MultiplePoseOdometry,
)
from phd.moduslam.frontend_manager.utils import fill_storage
from phd.moduslam.utils.exceptions import EmptyStorageError

logger = logging.getLogger(frontend_manager)


class Builder:
    """Creates multiple edges combinations and chooses the best one."""

    def __init__(self, handlers: set[Handler]):
        """
        Args:
            handlers: handlers for creating measurements.
        """
        self._handlers = handlers
        self._analyzer = MultiplePoseOdometry()
        self._candidate_factory = Factory()
        self._storage = MeasurementStorage()

    def create_graph(self, graph: Graph, data_batch: DataBatch) -> Graph:
        """Creates graph candidate using the measurements from the data batch.

        Args:
            graph: a main graph to use.

            data_batch: a data batch with elements.

        Returns:
            new graph elements.
        """

        while not data_batch.empty:

            fill_storage(self._storage, data_batch, self._handlers, self._analyzer)

            candidate = self._candidate_factory.create_best_candidate(graph, self._storage)

            self._storage.clear()

            if candidate.leftovers:
                self._storage.add(candidate.leftovers)

            return candidate.graph

        msg = "Input data batch is empty."
        logger.error(msg)
        raise EmptyStorageError(msg)
