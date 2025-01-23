import logging
from pathlib import Path

from src.bridge.optimal_candidate_factory import Factory
from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.logger.logging_config import frontend_manager
from src.measurement_storage.storage import MeasurementStorage
from src.moduslam.data_manager.batch_factory.batch import DataBatch
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.measurement_storage_analyzers.analyzers import (
    DoublePoseOdometry,
)
from src.moduslam.frontend_manager.utils import fill_storage

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
        self._output_dir = Path(__file__).parent / "graphs"
        self._create_output_dir(self._output_dir)

    def create_graph(self, graph: Graph, data_batch: DataBatch) -> Graph:
        """Creates graph candidate using the measurements from the data batch.

        Args:
            graph: a main graph.

            data_batch: a data batch with elements.

        Returns:
            a new graph.
        """
        storage = MeasurementStorage

        counter = 0
        while not data_batch.empty:

            fill_storage(storage, data_batch, self._handlers, self._analyzer)

            data = storage.data()
            candidate = self._candidate_factory.create_candidate(graph, data)

            storage.clear()

            if candidate.leftovers:
                logger.warning("Adding leftovers back to storage")
                for measurement in candidate.leftovers:
                    storage.add(measurement)

            graph = candidate.graph
            self.dump_graph(graph, counter, self._output_dir)
            counter += 1

        logger.info("Input data batch is empty.")
        return graph

    @staticmethod
    def dump_graph(graph: Graph, idx: int, output_dir: Path) -> None:
        """Dumps the graph to the file."""
        filename = output_dir / f"sub_{idx}.txt"
        values = graph.get_backend_instances()
        graph.factor_graph.saveGraph(str(filename), values)

    @staticmethod
    def _create_output_dir(directory: Path) -> None:
        """Creates the output directory if it does not exist."""
        if not directory.exists():
            directory.mkdir(parents=True)
        else:
            for file in directory.iterdir():
                if file.is_file():
                    file.unlink()
