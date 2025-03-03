"""A factory for creating edges between the pose and the landmark.
TODO: implement methods.
"""

from src.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from src.bridge.edge_factories.utils import create_new_vertices
from src.measurement_storage.measurements.pose_landmark import PoseLandmark
from src.moduslam.frontend_manager.main_graph.edges.pose2LandmarkPose import (
    PoseToLandmark,
)
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    Pose,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    PoseLandmark as LandmarkVertex,
)
from src.utils.auxiliary_dataclasses import TimeRange


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: PoseLandmark
    ) -> GraphElement[PoseToLandmark]:
        """Creates a new edge between the pose and a new or existing landmark.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a descriptor of the detected landmark.

        Returns:
            a new element.
        """
        t = measurement.timestamp

        pose = cls._get_pose_with_status()

        landmark = cls._get_landmark_with_status()

        edge = cls._create_edge(pose.instance, landmark.instance, measurement)

        new_vertices = create_new_vertices([pose, landmark])

        return GraphElement(edge, {pose.instance: t, landmark.instance: t}, new_vertices)

    @classmethod
    def _get_pose_with_status(cls) -> VertexWithStatus[Pose]:
        """Gets a new or existing pose vertex."""
        raise NotImplementedError

    @classmethod
    def _get_landmark_with_status(cls) -> VertexWithStatus[LandmarkVertex]:
        """Gets a new or existing landmark vertex."""
        raise NotImplementedError

    @classmethod
    def _create_edge(
        cls, pose: Pose, landmark: LandmarkVertex, measurement: PoseLandmark
    ) -> PoseToLandmark:
        """Creates a new edge with a new pose and the observed landmark."""
        raise NotImplementedError
