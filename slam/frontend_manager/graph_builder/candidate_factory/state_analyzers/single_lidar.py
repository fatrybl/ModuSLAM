import logging

from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.criteria.criterion_ABC import (
    Criterion,
)
from slam.frontend_manager.handlers.pointcloud_matcher import PointcloudMatcher

logger = logging.getLogger(__name__)


class SingleLidarStateAnalyzer(StateAnalyzer):
    """
    Analyzer for lidar states.
    """

    def __init__(self) -> None:
        self._handler: PointcloudMatcher
        self._criteria: list[Criterion] = []
        self._num_pointclouds: int = 1
        self._new_state: State | None = None

    @property
    def criteria(self) -> list[Criterion]:
        """
        All criteria.
        Returns:
            (list[Criterion]): list of criteria.
        """
        return self._criteria
