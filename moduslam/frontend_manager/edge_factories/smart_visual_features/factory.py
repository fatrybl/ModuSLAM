"""
    TODO: add tests
"""

from moduslam.frontend_manager.edge_factories.interface import EdgeFactory
from moduslam.frontend_manager.edge_factories.smart_visual_features.edges_factory import (
    EdgesFactory,
)
from moduslam.frontend_manager.edge_factories.smart_visual_features.storage import (
    VisualFeatureStorage,
)
from moduslam.frontend_manager.edge_factories.utils import get_last_vertex
from moduslam.frontend_manager.graph.custom_edges import SmartVisualFeature
from moduslam.frontend_manager.graph.custom_vertices import CameraPose, Pose
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.setup_manager.sensors_factory.sensors import StereoCamera
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
        self._name: str = config.name
        self._time_margin: int = sec2nanosec(config.search_time_margin)
        self._frame_limit: int = 10
        self._current_frame: int = 0
        self._storage = VisualFeatureStorage()
        self._factory = EdgesFactory()

    @property
    def name(self) -> str:
        """Unique factory name."""
        return self._name

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
        m = measurements.last
        sensor = m.elements[0].measurement.sensor
        visual_features = m.value

        # kp1 = cv2.KeyPoint()
        # kp1.pt = (1, 1)
        # kp2 = cv2.KeyPoint()
        # kp2.pt = (2, 2)
        # kp3 = cv2.KeyPoint()
        # kp3.pt = (3, 3)
        # kp4 = cv2.KeyPoint()
        # kp4.pt = (4, 4)
        # kp5 = cv2.KeyPoint()
        # kp5.pt = (5, 5)
        # desc1 = np.array([i * 1 for i in range(32)], dtype=np.uint8)
        # desc2 = np.array([i * 2 for i in range(32)], dtype=np.uint8)
        # desc3 = np.array([i * 3 for i in range(32)], dtype=np.uint8)
        # desc4 = np.array([i * 4 for i in range(32)], dtype=np.uint8)
        # desc5 = np.array([i * 5 for i in range(32)], dtype=np.uint8)
        # f1 = VisualFeature(kp1, desc1)
        # f2 = VisualFeature(kp2, desc2)
        # f3 = VisualFeature(kp3, desc3)
        # f4 = VisualFeature(kp4, desc4)
        # f5 = VisualFeature(kp5, desc5)
        # visual_features = [f1, f2, f3, f4, f5]

        if not isinstance(sensor, StereoCamera):
            raise TypeError(f"Expected {StereoCamera.__name__!r}, got {type(sensor)!r}")

        if self._current_frame == self._frame_limit:
            self._storage.remove_old_features()
            self._current_frame -= 1

        matches = self._storage.get_matches(visual_features)
        unmatched_features = self._storage.get_unmatched_features(visual_features, matches)

        pose = self._get_vertex(graph.vertex_storage, timestamp, self._time_margin)

        new_edges = self._factory.create_edges(m, pose, sensor, unmatched_features)

        for edge, feature in zip(new_edges, unmatched_features):
            self._storage.add(feature, edge)

        modified_edges = self._factory.modify_edges(
            self._storage.items, matches, visual_features, pose, m
        )

        self._current_frame += 1

        return new_edges + modified_edges

    @staticmethod
    def _get_vertex(storage: VertexStorage, timestamp: int, time_margin: int) -> CameraPose:
        """Gets vertex with the given timestamps.

        Args:
            storage: storage of vertices.

            timestamp: timestamp of the vertex.

            time_margin: time margin for the search.

        Returns:
            vertex.
        """
        cam_pose = get_last_vertex(CameraPose, storage, timestamp, time_margin)
        if cam_pose:
            return cam_pose

        pose = storage.find_closest_optimizable_vertex(Pose, timestamp, time_margin)
        if pose:
            cam_pose = CameraPose(timestamp=pose.timestamp, index=pose.index, value=pose.value)
            return cam_pose

        previous_cam_pose = storage.get_last_vertex(CameraPose)
        if previous_cam_pose:
            index = previous_cam_pose.index + 1
            cam_pose = CameraPose(index, timestamp, previous_cam_pose.value)
            return cam_pose

        new_index = generate_index(storage.index_storage)
        cam_pose = CameraPose(new_index, timestamp)
        return cam_pose
