from abc import ABC, abstractmethod

from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)


class CandidateAnalyzer(ABC):
    """Base abstract class for candidate analyzers.

    Analyzes a graph candidate if it is ready to be merged with Graph.
    """

    @abstractmethod
    def check_readiness(self, graph_candidate: GraphCandidate) -> bool:
        """Evaluates existing state(s) of a candidate and decides if it is ready to be
        merged with the graph.

        Args:
            graph_candidate: GraphCandidate instance to be analyzed.

        Returns:
            success/failure status of a new graph candidate.
        """
