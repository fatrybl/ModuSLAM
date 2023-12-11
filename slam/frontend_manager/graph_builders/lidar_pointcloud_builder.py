import logging
from typing import Optional

from slam.frontend_manager.elements_distributor.elements_distributor import MeasurementStorage
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builders.graph_builder_ABC import GraphBuilder

logger = logging.getLogger(__name__)


class PointCloudBuilder(GraphBuilder):
    """
    Build a graph for point-cloud based map.
    """

    def __init__(self, graph: Graph, config: Optional) -> None:
        self._graph: Graph = graph
        self.params = config
        self.candidate_factory = CandidateFactory()
        self.merger = GraphMerger()

    def graph_candidate_ready(self, ) -> bool:
        """
        Updates status of the graph candidate.
        Returns:
            status (bool): current readiness status of the graph candidate.
        """

        status: bool = self.candidate_factory.get_candidate_status()
        return status

    def process_storage(self, storage: MeasurementStorage) -> None:
        """
        Processes input measurements in order to add new states to the graph candidate.

        Args:
            storage (MeasurementStorage): measurements from Distributor.

        1) Analyze the measurements whether to add a new state or not.
        2) Add new state to the candidate if condition.
        """
        self.candidate_factory.state_analyzer.evaluate()
        if self.candidate_factory.state_analyzer.new_state_status:
            self.candidate_factory.add_state(storage)
