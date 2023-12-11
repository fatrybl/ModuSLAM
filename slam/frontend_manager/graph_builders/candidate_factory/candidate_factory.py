import logging

from slam.frontend_manager.elements_distributor.elements_distributor import MeasurementStorage
from slam.frontend_manager.graph.graph_candidate import GraphCandidate
from slam.frontend_manager.graph_builders.candidate_factory.candidate_analyzer import CandidateAnalyzer
from slam.frontend_manager.graph_builders.candidate_factory.state_analyzer import LidarStateAnalyzer

logger = logging.getLogger(__name__)


class CandidateFactory:
    """
    Creates graph candidate.
    """

    def __init__(self, ):
        self.graph_candidate = GraphCandidate()
        self.state_analyzer = LidarStateAnalyzer()
        self.candidate_analyzer = CandidateAnalyzer()

    def _create_state(self, storage: MeasurementStorage) -> None:
        """
        Creates a new state based on the given measurements storage.
        Args:
            storage: a storage with the processed measurements.
        """
        pass

    def add_state(self, storage: MeasurementStorage) -> None:
        """
        Adds new state to the graph candidate based on measurements in the storage.
        Resets state status.
        """
        new_state = self._create_state(storage)
        self.graph_candidate.states += new_state
        self.state_analyzer.new_state_status = False

    def get_candidate_status(self) -> bool:
        """
        Gets the graph candidate status after analysis.
        Returns:
            status (bool): graph candidate readiness status.
        """
        status: bool = self.candidate_analyzer.check_readiness(self.graph_candidate)
        return status
