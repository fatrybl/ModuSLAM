import logging

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)

logger = logging.getLogger(__name__)


class ImuPreintegrator(StateAnalyzer):
    """Analyzer for lidar states."""

    def __init__(self, config: StateAnalyzerConfig) -> None:
        super().__init__(config)

    def evaluate(self, storage: MeasurementStorage) -> State | None:
        raise NotImplementedError
