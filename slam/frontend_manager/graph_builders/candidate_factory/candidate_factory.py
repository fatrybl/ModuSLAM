import logging

from slam.frontend_manager.elements_distributor.elements_distributor import (
    MeasurementStorage,
)
from slam.frontend_manager.graph.graph_candidate import GraphCandidate, State
from slam.frontend_manager.graph_builders.candidate_factory.candidate_analyzer_ABC import (
    CandidateAnalyzer,
)
from slam.frontend_manager.graph_builders.candidate_factory.state_analyzers.single_lidar import (
    SingleLidarStateAnalyzer,
)

logger = logging.getLogger(__name__)


class CandidateFactory:
    """
    Creates a graph candidate.
    """

    def __init__(
        self,
    ):
        self.graph_candidate = GraphCandidate()
        self.state_analyzer = SingleLidarStateAnalyzer()
        self.candidate_analyzer = CandidateAnalyzer()

    def add_state(self, storage: MeasurementStorage) -> None:
        """
        Adds new state to the graph candidate based on measurements in the storage.
        Resets state status.
        """
        new_state: State = State(storage)
        self.graph_candidate.states.append(new_state)
        self.state_analyzer.new_state_status = False

    def get_candidate_status(self) -> bool:
        """
        Gets the graph candidate status after analysis.
        Returns:
            status (bool): graph candidate readiness status.
        """
        status: bool = self.candidate_analyzer.check_readiness(self.graph_candidate)
        return status
