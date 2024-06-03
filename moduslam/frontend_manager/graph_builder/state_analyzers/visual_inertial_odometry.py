from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    State,
)
from moduslam.frontend_manager.graph_builder.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from moduslam.frontend_manager.handlers.visual_odometry.odometry_generator import (
    VisualOdometry,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from moduslam.utils.ordered_set import OrderedSet


class VisualInertialOdometryAnalyzer(StateAnalyzer):
    """Analyzer for visual odometry measurements` handler.

    Adds new state if the storage contains a measurement with visual pointcloud
    odometry.
    """

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)
        self._state = State()
        self._update_state = False

    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates a storage and creates a state if conditions are satisfied.

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

        if isinstance(m.handler, VisualOdometry):
            self._update_state = True
            return self._state
        else:
            return None
