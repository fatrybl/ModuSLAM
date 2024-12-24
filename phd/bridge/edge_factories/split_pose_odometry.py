from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.pose_odometry import Factory as OdometryFactory
from phd.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.utils.auxiliary_dataclasses import TimeRange
from phd.utils.exceptions import SkipItemException


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: SplitPoseOdometry,
    ) -> GraphElement[PoseOdometry]:
        """Create a new edge for split odometry if the measurement's timestamp matches
        the parent measurement stop timestamp.

        Args:
            graph: a main graph.

            clusters: a table with current clusters and time ranges.

            clusters: clusters with time ranges.

            measurement: a split odometry measurement.

        Returns:
            a new element.

        Raises:
            SkipItemException: if the measurement's timestamp does not match
            the parent measurement stop timestamp.
        """
        stop = measurement.parent.time_range.stop

        if measurement.timestamp == stop:
            element = OdometryFactory.create(graph, clusters, measurement.parent)
            return element

        else:
            raise SkipItemException
