"""TODO: implement."""

from moduslam.bridge.edge_factories.factory_protocol import EdgeFactory
from moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.utils.auxiliary_dataclasses import TimeRange, VisualFeature


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: VisualFeature,
    ) -> list[GraphElement]:
        raise NotImplementedError
