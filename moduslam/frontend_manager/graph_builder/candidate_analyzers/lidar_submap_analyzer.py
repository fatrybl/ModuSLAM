from moduslam.frontend_manager.graph_builder.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from moduslam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher


class LidarSubmapAnalyzer(CandidateAnalyzer):
    """Simple analyzer for lidar pointcloud sub-map candidate."""

    def __init__(self):
        self._num_required_states: int = 1

    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """Checks graph candidate if readiness criterion is satisfied.
        Criterion: 1 state with lidar pointcloud is present in the candidate.

        Returns:
            status: the readiness status.
        """
        return len(graph_candidate.states) == self._num_required_states


class LidarSubmapAnalyzer1(CandidateAnalyzer):
    """Simple analyzer for lidar pointcloud sub-map candidate.

    TODO: add to system.
    """

    def __init__(self):
        self._num_required_states: int = 2

    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """Checks graph candidate if readiness criterion is satisfied.
        Criterion: 1 state with lidar pointcloud is present in the candidate.

        Returns:
            status: the readiness status.
        """
        for state in graph_candidate.states:
            for handler, measurements in state.data.items():
                if isinstance(handler, ScanMatcher) and measurements:
                    return True

        return False
