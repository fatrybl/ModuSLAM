import logging

from slam.frontend_manager.element_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
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
from slam.setup_manager.tables_initializer import init_handler_state_analyzer_table

logger = logging.getLogger(__name__)


<<<<<<<< HEAD:slam/frontend_manager/graph_builder/candidate_factory/factories/lidar_submap.py
class LidarMapCandidateFactory(CandidateFactory):
    """Creates graph candidate with lidar point-cloud keyframe(s)."""

    def __init__(self) -> None:
        self._graph_candidate: GraphCandidate = GraphCandidate()
        self._candidate_analyzer: CandidateAnalyzer = LidarSubmapAnalyzer()
        self._previous_measurement: Measurement | None = None
        self._table: dict[Handler, StateAnalyzer] = {}

    def init_table(self, config: dict[str, str]) -> None:
        """
        Initializes the table: handler -> state analyzer.

        Args:
            config (dict[str, str]): table with names of handlers and state analyzers.

        """
        self._table = init_handler_state_analyzer_table(config)
========
class LidarSubmapCandidateFactory(CandidateFactory):
    """Creates graph candidate with lidar point-cloud keyframe(s)."""

    def __init__(self):
        self._graph_candidate: GraphCandidate = GraphCandidate()
        self._candidate_analyzer: CandidateAnalyzer = LidarSubmapAnalyzer()
        self._handler_analyzer_table: dict[Handler, StateAnalyzer] = {}
        self._previous_measurement: Measurement | None = None

    def _fill_table(self, config) -> None:
        """Fills handler-analyzer table based on the given config.

        Args:
            config (dict[str, str]): names of handlers and corresponding analyzers.
        """
        for handler_name, analyzer_name in config.items():
            handler: Handler = HandlerFactory.get_handler(handler_name)
            analyzer: StateAnalyzer = StateAnalyzerFactory.get_analyzer(analyzer_name)
            self._handler_analyzer_table[handler] = analyzer
>>>>>>>> 3e68bcf (UPD: save current progress):slam/frontend_manager/graph_builder/candidate_factory/factories/lidar_keyframe.py

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
        """
        raise NotImplementedError

    def process_storage(self, storage: MeasurementStorage) -> None:
        """Processes input measurements and adds new states to the graph candidate if a
        criterion is satisfied. Storage satisfies only 1 criterion in time.

        1) Takes last measurement from the storage.
        2) If the measurement is new: not equal to the previous one:
            3) Distribute it to the corresponding state analyzer based on its handler.
            4) The analyzer decides if a new state should be added to the graph candidate.
            5) if new state: add it to the graph candidate.
            6) Update the previous measurement.


        Args:
            storage (MeasurementStorage): processed measurements from the Element Distributor.
        """
        try:
            new_measurement = storage.recent_measurement
        except IndexError:
            msg = "Empty storage: no measurements to process."
            logger.debug(msg)
            return

<<<<<<<< HEAD:slam/frontend_manager/graph_builder/candidate_factory/factories/lidar_submap.py
        if self._previous_measurement and self._previous_measurement == new_measurement:
            return

        else:
            analyzer = self._table[new_measurement.handler]
            new_state: State | None = analyzer.evaluate(storage)

            if new_state:
                self._graph_candidate.states.append(new_state)

            self._previous_measurement = new_measurement
========
        else:
            if new_measurement != self._previous_measurement:
                self._previous_measurement = new_measurement
                analyzer = self._handler_analyzer_table[new_measurement.handler]
                new_state: State | None = analyzer.evaluate(storage)

                if new_state:
                    self._graph_candidate.states.append(new_state)
>>>>>>>> 3e68bcf (UPD: save current progress):slam/frontend_manager/graph_builder/candidate_factory/factories/lidar_keyframe.py
