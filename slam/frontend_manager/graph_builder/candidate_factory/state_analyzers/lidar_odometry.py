import logging

from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.frontend_manager.measurement_storage import MeasurementStorage
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)

logger = logging.getLogger(__name__)


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
        self._handler: Handler = HandlersFactory.get_handler(config.handler_name)

    def evaluate(self, storage: MeasurementStorage) -> State | None:
        """Evaluates the storage and decides whether to add a new state.

        Args:
            storage: a storage with measurements.

        Returns:
            new state or None.
        """
        last_measurement = storage.data[self._handler][-1]
        new_state = State()
        new_state.add(last_measurement)
        return new_state
