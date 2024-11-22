from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.moduslam.frontend_manager.main_graph.edges.custom import SmartVisualFeature
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange, VisualFeature


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: VisualFeature,
    ) -> list[GraphElement]:
        #
        # elements: list[GraphElement] = []
        #
        # existing_pose = cluster.get_latest_vertex(cls._vertex_type)
        #
        # if existing_pose:
        #     current_pose = existing_pose
        # else:
        #     current_pose = create_new_vertex(cls._vertex_type, graph)
        #
        # for feature in measurement.features:
        #
        #     similar_feature = cls._get_similar_point(feature, graph.vertex_storage)
        #
        #     if similar_feature:
        #         new_edge = cls._modify_edge(similar_feature, feature, current_pose)
        #     else:
        #         new_edge = cls._create_new_edge(feature, current_pose)
        #
        #     element = cls._create_graph_element(new_edge, current_pose, measurement.timestamp)
        #     elements.append(element)
        #
        # return elements
        raise NotImplementedError

    @classmethod
    def _create_new_edge(cls, feature: VisualFeature, current_pose: Pose) -> SmartVisualFeature:
        """Creates a new edge with a new pose and the observed visual feature."""
        raise NotImplementedError

    @classmethod
    def _create_graph_element(
        cls, edge: SmartVisualFeature, vertex: Pose, timestamp: float
    ) -> GraphElement:
        raise NotImplementedError

    @classmethod
    def _get_similar_point(
        cls, feature: VisualFeature, storage: VertexStorage
    ) -> SmartVisualFeature | None:
        """Finds an edge with the similar visual feature in the graph.

        Args:
            graph: a main graph with points.

            feature: the visual feature to find a similar one to.

        Returns:
            an existing edge.
        """
        raise NotImplementedError

    @classmethod
    def _modify_edge(
        cls, edge: SmartVisualFeature, feature: VisualFeature, current_pose: Pose
    ) -> SmartVisualFeature:
        """Modifies the edge by adding a new pose with a new observed visual feature."""
        raise NotImplementedError
