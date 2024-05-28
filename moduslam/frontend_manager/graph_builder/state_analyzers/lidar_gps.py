from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    State,
)
from moduslam.frontend_manager.graph_builder.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from moduslam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from moduslam.frontend_manager.handlers.vrs_gps import VrsGpsPreprocessor
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from moduslam.utils.ordered_set import OrderedSet


class LidarGpsAnalyzer(StateAnalyzer):
    """Analyzer for lidar pointcloud odometry, IMU odometry, GPS position measurements`
    handlers."""

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)
        self._state = State()
        self._update_state = False
        self._lidar_odometry_handlers: set[ScanMatcher] = set()

    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates a storage and creates a state if conditions are satisfied.

        Args:
            measurements: an ordered set of measurements.

        Returns:
            new state or None.
        """
        if self._update_state:
            self._clear()

        m = measurements.last
        self._state.add(m)

        if isinstance(m.handler, ScanMatcher):
            self._update_state = True
            return self._state

        if isinstance(m.handler, VrsGpsPreprocessor):
            self._update_state = True
            return self._state

        else:
            return None

    def _clear(self) -> None:
        """Clears the analyzer state."""
        self._state = State()
        self._lidar_odometry_handlers.clear()
        self._update_state = False
