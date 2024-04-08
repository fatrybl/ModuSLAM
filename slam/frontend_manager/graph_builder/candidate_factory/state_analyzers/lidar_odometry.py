import logging

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)

logger = logging.getLogger(__name__)


class LidarOdometryStateAnalyzer(StateAnalyzer):
    """Analyzer for lidar odometry measurements` handler."""

    def __init__(self, config: StateAnalyzerConfig) -> None:
        super().__init__(config)
        self._handler: Handler = HandlersFactory.get_handler(config.handler_name)

    def evaluate(self, storage: MeasurementStorage) -> State | None:
        """
        Evaluates the state based on the given storage.
        Args:
            storage (MeasurementStorage): storage of measurements.

        Returns:
            (State | None): state of the graph candidate if it is ready,
                            otherwise None.
        """
        last_measurement = storage.data[self._handler][-1]
        new_state = State()
        new_state.add(last_measurement)
        return new_state
