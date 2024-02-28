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
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.handlers_factory.factory import HandlerFactory
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzerFactory

logger = logging.getLogger(__name__)


class PointcloudFactory(CandidateFactory):
    """Creates graph candidate with lidar point cloud.

    pre-setup:
        1) Distributing table (dict) should be initialized.
    """

    def __init__(
        self,
    ):
        self._graph_candidate: GraphCandidate = GraphCandidate()
        self._candidate_analyzer: CandidateAnalyzer = PointcloudCandidateAnalyzer()
        self._handler_analyzer_table: dict[Handler, StateAnalyzer] = {}

    def _fill_table(self, config) -> None:
        """Fills handler-analyzer table based on the given config."""
        for handler_name, analyzer_name in config.items():
            handler: Handler = HandlerFactory.get_handler(handler_name)
            analyzer: StateAnalyzer = StateAnalyzerFactory.get_analyzer(analyzer_name)
            self._handler_analyzer_table[handler] = analyzer

    @property
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate.

        Returns:
            (GraphCandidate): graph candidate.
        """
        return self._graph_candidate

    def candidate_ready(self) -> bool:
        """Candidate readiness status.

        Returns:
            (bool): graph candidate readiness status.
        """
        return self._candidate_analyzer.check_readiness(self._graph_candidate)

    def synchronize_states(self) -> None:
        """Synchronizes states of the graph candidate.

        input: list[State] of size N
        output: list[State] of size M, N >= M
        TODO: implement synchronization of states.
        """
        ...

    def process_storage(self, storage: MeasurementStorage) -> None:
        """Processes input measurements and adds new states to the graph candidate if a
        criterion is satisfied. Storage satisfies only 1 criterion in time.

        1) Take last measurement from the storage.
        2) Distribute it to the corresponding state analyzer based on its handler.
        3) The analyzer decides if a new state should be added to the graph candidate.
        4) if new state: add it to the graph candidate.


        Args:
            storage (MeasurementStorage): processed measurements from the Distributor.
        """

        measurement = storage.recent_measurement
        if measurement is not None:
            analyzer = self._handler_analyzer_table[measurement.handler]
            new_state: State | None = analyzer.evaluate(storage)

            if new_state is not None:
                self._graph_candidate.states.append(new_state)
