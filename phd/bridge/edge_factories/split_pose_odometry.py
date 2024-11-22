from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.pose_odometry import Factory as OdometryFactory
from phd.bridge.edge_factories.utils import get_cluster
from phd.bridge.objects.auxiliary_classes import SplitPoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import SkipItemException


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: SplitPoseOdometry,
    ) -> GraphElement:
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
        start = measurement.parent.time_range.start
        stop = measurement.parent.time_range.stop

        if measurement.timestamp == stop:
            element = OdometryFactory.create(graph, clusters, measurement.parent)
            return element

        else:
            cls._try_copy_pose_i(graph.vertex_storage, clusters, start)
            raise SkipItemException

    @classmethod
    def _try_copy_pose_i(
        cls, storage: VertexStorage, clusters: dict[VertexCluster, TimeRange], timestamp: int
    ) -> None:
        """Tries to add an i-th pose to the clusters if it exists in the storage.

        Args:
            storage: a storage with vertices.

            clusters: a table with clusters and time ranges.

            timestamp: a timestamp.
        """
        cluster = get_cluster(clusters, timestamp)
        pose = cls._find_pose_i(storage, cluster, timestamp)
        if pose:
            cluster.add(pose, timestamp)

    @classmethod
    def _find_pose_i(
        cls, storage: VertexStorage, cluster: VertexCluster, timestamp: int
    ) -> Pose | None:
        """Finds the pose in the storage based on timestamp if it exists and not it the
        given cluster.

        Args:
            storage: a storage with vertices.

            cluster: a cluster to find the pose in.

            timestamp: a timestamp.

        Returns:
            existing pose in the storage or None.
        """
        pose = cluster.get_latest_vertex(Pose)

        if not pose:
            existing_cluster = storage.get_cluster(timestamp)
            if existing_cluster:
                pose = existing_cluster.get_latest_vertex(Pose)
                if pose:
                    return pose
        return None
