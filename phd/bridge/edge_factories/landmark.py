from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.measurements.processed_measurements import PoseLandmark as DetectedLandmark
from phd.moduslam.frontend_manager.main_graph.edges.custom import PoseToLandmark
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement, VerticesTable
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose, PoseLandmark


class Factory(EdgeFactory):

    _vertex_type1 = Pose
    _vertex_type2 = PoseLandmark

    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement: DetectedLandmark
    ) -> GraphElement:

        existing_pose = cluster.get_latest_vertex(cls._vertex_type1)

        if existing_pose:
            current_pose = existing_pose
        else:
            current_pose = create_new_vertex(cls._vertex_type1, graph)

        similar_landmark = cls._get_similar_landmark(measurement.descriptor, graph.vertex_storage)

        if similar_landmark:
            landmark = similar_landmark
        else:
            landmark = create_new_vertex(cls._vertex_type2, graph)

        edge = cls._create_edge(current_pose, landmark, measurement)

        new_vertices = cls._get_new_vertices()

        element = GraphElement(edge, new_vertices)
        return element

    @classmethod
    def _get_new_vertices(cls) -> VerticesTable:
        raise NotImplementedError

    @classmethod
    def _get_similar_landmark(
        cls, descriptor: tuple[int, ...], storage: VertexStorage
    ) -> PoseLandmark:
        """Finds a similar landmark in the graph based on the distance between the
        landmarks."""
        raise NotImplementedError

    @classmethod
    def _create_edge(
        cls, pose: Pose, landmark: PoseLandmark, measurement: DetectedLandmark
    ) -> PoseToLandmark:
        raise NotImplementedError

    @classmethod
    def _create_element(
        cls, edge: PoseToLandmark, new_vertices: tuple[Pose | PoseLandmark, ...] | None = None
    ) -> GraphElement:
        raise NotImplementedError
