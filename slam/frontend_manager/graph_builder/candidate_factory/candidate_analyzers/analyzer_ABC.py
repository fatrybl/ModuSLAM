from abc import ABC, abstractmethod

from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)


class CandidateAnalyzer(ABC):
    """
    Analyzes states. Checks if a graph candidate is ready to be merged with Graph.
    """

    @abstractmethod
    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """
        Evaluates existing state(s) and decides whether the criteria of a new graph candidate are satisfied.

        Returns: success/failure status of a new graph candidate.
        """
