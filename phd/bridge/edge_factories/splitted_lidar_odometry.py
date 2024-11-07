from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.pose_odometry import Factory as OdometryFactory
from phd.exceptions import SkipItemException
from phd.external.objects.measurements import SplitPoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement: SplitPoseOdometry
    ) -> GraphElement:
        """Create a new edge for split odometry if the measurement's timestamp matches
        the parent measurement stop timestamp.

        Args:
            graph: a main graph.

            cluster: a vertex cluster.

            measurement: a split odometry measurement.

        Returns:
            a new element.

        Raises:
            SkipItemException: if the measurement's timestamp does not match
            the parent measurement stop timestamp.
        """
        if measurement.timestamp == measurement.parent.time_range.stop:
            element = OdometryFactory.create(graph, cluster, measurement)
            return element

        raise SkipItemException
