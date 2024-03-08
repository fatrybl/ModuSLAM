from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)


class LidarSubmapAnalyzer(CandidateAnalyzer):
    """Decides if an amount of states with point clouds is enough to be form a
    candidate.

    For simplicity, the analyzer checks if the only 1 state is present in the candidate.
    """

    def __init__(self):
        self.num_required_states: int = 1

    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """Checks graph candidate if readiness criteria are satisfied.

        Returns:
            status (bool): the status of a candidate.
        """
        return len(graph_candidate.states) == self.num_required_states
