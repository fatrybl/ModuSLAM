from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from slam.frontend_manager.measurement_storage import Measurement
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarInertialOdometryStateAnalyzer(StateAnalyzer):

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
        present. If IMU odometry is present, it is added to the state.

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

        if isinstance(m.handler, ScanMatcher):
            self._update_state = True
            return self._state
        else:
            return None
