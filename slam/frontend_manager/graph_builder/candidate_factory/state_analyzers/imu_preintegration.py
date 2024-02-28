import logging

from configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.imu_preintegration import ImuPreintegration

logger = logging.getLogger(__name__)


class ImuPreintegrator(StateAnalyzer):
    """Analyzer for lidar states."""

    def __init__(self, config: StateAnalyzerConfig) -> None:
        self._name: str = config.name
        self._handler_type: type = ImuPreintegration
        self._new_state: State | None = None

    @property
    def name(self) -> str:
        """Name of the analyzer.

        Returns:
            (str): name of the analyzer.
        """
        return self._name

    def evaluate(self, storage: MeasurementStorage) -> State | None: ...
