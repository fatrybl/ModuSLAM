import logging

from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.analyzer_ABC import (
    CandidateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.lidar_submap_analyzer import (
    LidarSubmapAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.factories.factory_ABC import (
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
from slam.frontend_manager.measurement_storage import Measurement, MeasurementStorage
from slam.setup_manager.tables_initializer import init_handler_state_analyzer_table
from slam.utils.exceptions import EmptyStorageError

logger = logging.getLogger(__name__)


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
        try:
            new_measurement = storage.recent_measurement
        except EmptyStorageError:
            msg = "Empty storage: no measurements to process."
            logger.debug(msg)
            return

        if self._previous_measurement and self._previous_measurement == new_measurement:
            return

        else:
            analyzer = self._table[new_measurement.handler]
            new_state: State | None = analyzer.evaluate(storage)

            if new_state:
                self._graph_candidate.states.append(new_state)

            self._previous_measurement = new_measurement
