from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)


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
