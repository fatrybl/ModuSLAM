from moduslam.frontend_manager.graph_builder.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from moduslam.frontend_manager.graph_builder.candidate_analyzers.lidar_submap_analyzer import (
    LidarSubmapAnalyzer,
)
from moduslam.frontend_manager.graph_builder.candidate_factory.factory_ABC import (
    CandidateFactory,
)
from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
    State,
)
from moduslam.frontend_manager.graph_builder.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from moduslam.frontend_manager.handlers.ABC_handler import Handler
from moduslam.frontend_manager.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from moduslam.setup_manager.tables_initializer import init_handler_state_analyzer_table


class LidarMapCandidateFactory(CandidateFactory):
    """Creates graph candidate with lidar pointcloud keyframe(s)."""

    def __init__(self) -> None:
        self._graph_candidate: GraphCandidate = GraphCandidate()
        self._candidate_analyzer: CandidateAnalyzer = LidarSubmapAnalyzer()
        self._previous_measurement: Measurement | None = None
        self._table: dict[Handler, StateAnalyzer] = {}

    @property
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate to be merged with the graph."""
        return self._graph_candidate

    def init_table(self, config: dict[str, str]) -> None:
        """Initializes "handler -> state analyzer" table.

        Args:
            config: config with "handler name -> state analyzer name" table.
        """
        self._table = init_handler_state_analyzer_table(config)

    def candidate_ready(self) -> bool:
        """Candidate readiness status."""
        return self._candidate_analyzer.check_readiness(self._graph_candidate)

    def synchronize_states(self) -> None:
        """Synchronizes states of the graph candidate.

        Not implemented.
        """
        raise NotImplementedError

    def process_storage(self, storage: MeasurementStorage) -> None:
        """Processes the storage with measurements and adds new states to the graph
        candidate if needed.

        Args:
            storage: storage with measurements.
        """
        if storage.empty:
            return None
        else:
            new_measurement = storage.recent_measurement

        if self._previous_measurement and self._previous_measurement == new_measurement:
            return None

        else:
            analyzer = self._table[new_measurement.handler]
            measurements = storage.data[new_measurement.handler]
            new_state: State | None = analyzer.evaluate(measurements)

            if new_state:
                self._graph_candidate.add(new_state)

            self._previous_measurement = new_measurement
