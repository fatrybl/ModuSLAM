from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.measurement_storage import Measurement
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarOdometryStateAnalyzer(StateAnalyzer):
    """Analyzer for lidar odometry measurements` handler.

    Adds new state if the storage contains a measurement with lidar pointcloud odometry.
    """

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)

    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates the storage and adds a new state if a lidar odometry measurement is
        present.

        Args:
            measurements: an ordered set of measurements.

        Returns:
            new state or None.
        """
        state = State()
        state.add(measurements.last)
        return state
