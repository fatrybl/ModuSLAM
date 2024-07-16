"""
    TODO: add tests
"""

from moduslam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from moduslam.frontend_manager.edge_factories.smart_visual_features.smart_factor import (
    VisualSmartFactorFactory,
)
from moduslam.frontend_manager.edge_factories.smart_visual_features.storage import (
    VisualFeatureStorage,
)
from moduslam.frontend_manager.edge_factories.smart_visual_features.utils import (
    create_edges,
    get_vertex,
)
from moduslam.frontend_manager.graph.custom_edges import SmartVisualFeature
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.utils.auxiliary_methods import sec2nanosec
from moduslam.utils.ordered_set import OrderedSet


class SmartVisualFeaturesFactory(EdgeFactory):
    """Creates edges of type VisualOdometry."""

    def __init__(self, config: EdgeFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        super().__init__(config)
        self._time_margin: int = sec2nanosec(config.search_time_margin)
        self._feature_storage = VisualFeatureStorage()
        self._smart_factor_factory = VisualSmartFactorFactory()
        self._frame_limit: int = 10
        self._current_frame: int = 0

    def create(
        self, graph: Graph, measurements: OrderedSet[Measurement], timestamp: int
    ) -> list[SmartVisualFeature]:
        """Creates 1 edge (VisualOdometry) with the given measurements.

        Args:
            graph: the graph to create the edge for.

            measurements: a measurement with visual features.

            timestamp: timestamp of the camera pose.

        Returns:
            list with 1 edge.
        """
        if self._current_frame == self._frame_limit:
            self._feature_storage.remove_old_features()
            self._current_frame -= 1

        m = measurements.last
        pose = get_vertex(graph.vertex_storage, timestamp, self._time_margin)
        edges = create_edges(pose, m, self._feature_storage, self._smart_factor_factory)
        self._current_frame += 1

        return edges
