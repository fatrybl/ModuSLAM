from phd.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from phd.bridge.edge_factories.utils import get_new_items
from phd.measurements.processed_measurements import PoseLandmark as DetectedLandmark
from phd.moduslam.frontend_manager.main_graph.edges.pose2LandmarkPose import (
    PoseToLandmark,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose, PoseLandmark
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: DetectedLandmark
    ) -> GraphElement:
        """Creates a new edge between the pose and a new or existing landmark.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a descriptor of the detected landmark.

        Returns:
            a new element.
        """
        pose = cls._get_pose_with_status()

        landmark = cls._get_landmark_with_status()

        edge = cls._create_edge(pose.instance, landmark.instance, measurement)

        new_vertices = get_new_items([pose, landmark])

        element = GraphElement(edge, new_vertices)
        return element

    @classmethod
    def _get_pose_with_status(cls) -> VertexWithStatus[Pose]:
        """Gets a new or existing pose vertex."""
        raise NotImplementedError

    @classmethod
    def _get_landmark_with_status(cls) -> VertexWithStatus[PoseLandmark]:
        """Gets a new or existing landmark vertex."""
        raise NotImplementedError

    @classmethod
    def _create_edge(
        cls, pose: Pose, landmark: PoseLandmark, measurement: DetectedLandmark
    ) -> PoseToLandmark:
        """Creates a new edge with a new pose and the observed landmark."""
        raise NotImplementedError
