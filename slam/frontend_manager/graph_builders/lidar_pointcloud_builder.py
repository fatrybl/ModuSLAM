import logging

from omegaconf import OmegaConf

from slam.frontend_manager.elements_distributor.elements_distributor import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builders.candidate_factory.candidate_factory import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builders.graph_merger.graph_merger import GraphMerger

logger = logging.getLogger(__name__)


class PointCloudBuilder(GraphBuilder):
    """
    Build a graph for point-cloud based map.
    """

    def __init__(self, config: OmegaConf | None = None) -> None:
        self._params = config
        self._candidate_factory = CandidateFactory()
        self._merger = GraphMerger()

    @property
    def candidate_merger(self) -> GraphMerger:
        return self._merger

    @property
    def candidate_factory(self) -> CandidateFactory:
        return self._candidate_factory

    def graph_candidate_ready(
        self,
    ) -> bool:
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
        self.candidate_factory.state_analyzer.evaluate(storage)
        new_state_ready: bool = self.candidate_factory.state_analyzer.new_state_status
        if new_state_ready:
            self.candidate_factory.add_state(storage)
