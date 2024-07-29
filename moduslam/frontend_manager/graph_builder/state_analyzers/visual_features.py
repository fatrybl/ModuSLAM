from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    State,
)
from moduslam.frontend_manager.graph_builder.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from moduslam.utils.ordered_set import OrderedSet


class VisualFeaturesAnalyzer(StateAnalyzer):
    """Analyzer for the measurements from key-points detector handler.

    Adds new state if the storage contains a measurement with visual pointcloud
    odometry.
    """

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)

    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates a storage and creates a state if conditions are satisfied.

        Args:
            measurements: an ordered set of measurements.

        Returns:
            new state or None.
        """
        state = State()
        state.add(measurements.last)
        return state
