from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.measurement_storage import Measurement
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.utils.ordered_set import OrderedSet


class MultipleLidarOdometryStateAnalyzer(StateAnalyzer):
    """Analyzer for odometry measurements` handler for multiple lidars."""

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)
        self._state = State()
        self._update_state = False

    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates the storage and adds a new state if a lidar odometry measurement is
        present.

        Args:
            measurements: an ordered set of measurements.

        Returns:
            new state or None.
        """
        if self._update_state:
            self._state.clear()
            self._update_state = False

        m = measurements.last
        self._state.add(m)

        if len(self._state.data) == 2:
            self._update_state = True
            return self._state
        else:
            return None
