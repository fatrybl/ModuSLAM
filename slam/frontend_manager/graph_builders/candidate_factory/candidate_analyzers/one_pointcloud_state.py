from slam.frontend_manager.graph.graph_candidate import GraphCandidate
from slam.frontend_manager.graph_builders.candidate_factory.candidate_analyzer_ABC import (
    CandidateAnalyzer,
)


class PointcloudCandidateAnalyzer(CandidateAnalyzer):
    def __init__(self):
        self.required_num_states = 1

    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """
        Checks if a state with a point-cloud based measurement exists.
        Returns:
            status (bool): the status of a candidate.
        """
        num_states = len(graph_candidate.states)
        if num_states == self.required_num_states:
            return True
        else:
            return False
