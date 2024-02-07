from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
    State,
)


class PointcloudCandidateAnalyzer(CandidateAnalyzer):
    """
    Decides if an amount of states with point clouds is enough to be merged with main graph.

    TODO: implement the logic.
    """

    def __init__(self):
        self._required_states: list[State] = []

    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """
        Check a candidate with different criteria.
        Returns:
            status (bool): the status of a candidate.
        """
        return graph_candidate.states in self._required_states
