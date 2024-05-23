from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from slam.frontend_manager.measurement_storage import Measurement
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarInertialOdometryStateAnalyzer(StateAnalyzer):
    """Analyzer for lidar & IMU odometry measurements` handlers."""

    num_handlers: int = 1  # number of different lidar pointcloud handlers in state.

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
            self._lidar_odometry_handlers.add(m.handler)

        if len(self._lidar_odometry_handlers) == self.num_handlers:
            self._update_state = True
            return self._state
        else:
            return None

    def _clear(self) -> None:
        """Clears the analyzer state."""
        self._state.clear()
        self._lidar_odometry_handlers.clear()
        self._update_state = False
