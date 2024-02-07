import logging

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.one_pointcloud_state import (
    PointcloudCandidateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.factory_ABC import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
    State,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.single_lidar import (
    SingleLidarStateAnalyzer,
)

logger = logging.getLogger(__name__)


class PointcloudFactory(CandidateFactory):
    """
    Creates graph candidate with lidar point cloud.
    """

    def __init__(
        self,
    ):
        self._graph_candidate: GraphCandidate = GraphCandidate()
        self._candidate_analyzer: CandidateAnalyzer = PointcloudCandidateAnalyzer()
        self._state_analyzer: StateAnalyzer = SingleLidarStateAnalyzer()

    @property
    def graph_candidate(self) -> GraphCandidate:
        """
        Graph candidate.

        Returns:
            (GraphCandidate): graph candidate.
        """
        return self._graph_candidate

    def candidate_ready(self) -> bool:
        """
        Candidate readiness status.

        Returns:
            (bool): graph candidate readiness status.
        """
        return self._candidate_analyzer.check_readiness(self._graph_candidate)

    def synchronize_states(self) -> None:
        """
        Synchronizes states of the graph candidate.
        input: list[State] of size N
        output: list[State] of size M, N >= M
        TODO: implement synchronization of states.
        """
        ...

    def process_storage(self, storage: MeasurementStorage) -> None:
        """
        Processes input measurements and adds new states to the graph candidate if a criterion is satisfied.
        Storage satisfies only 1 criterion in time.

        1) Check if a criterion for a new state is met for every criteria.
        2) If a criterion is met, add a new state to the graph candidate.

        Args:
            storage (MeasurementStorage): processed measurements from the Distributor.

        TODO: is break really necessary?
              One criterion == one state ?
        """

        for criterion in self._state_analyzer.criteria:
            if criterion.check(storage):
                new_state: State = State(storage)
                self._graph_candidate.states.append(new_state)
                break
