"""TODO: add tests and check integration with bias. Values are strange."""

import gtsam

from src.bridge.edge_factories.factory_protocol import EdgeFactory
from src.bridge.edge_factories.imu_odometry.utils import get_integrated_measurement
from src.bridge.edge_factories.utils import (
    create_new_vertices,
    create_vertex_i_with_status,
    create_vertex_j_with_status,
    get_cluster_for_timestamp_from_dict,
    get_cluster_for_timestamp_from_iterable,
)
from src.measurement_storage.measurements.imu import ContinuousImu, ProcessedImu
from src.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity4x4, zero_vector3


class Factory(EdgeFactory):

    timescale_factor: float = 1e-9
    _gravity: float = 9.81
    _params = gtsam.PreintegrationParams.MakeSharedU(_gravity)

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: ContinuousImu[ProcessedImu],
    ) -> GraphElement[ImuOdometry]:
        """Creates a new ImuOdometry edge with pre-integrated IMU factor.

        Args:
            graph: a main graph.

            clusters: a table with current clusters and time ranges.

            measurement: an IMU measurement.

        Returns:
            new element.
        """
        start = measurement.time_range.start
        stop = measurement.time_range.stop
        storage = graph.vertex_storage
        zero_bias = (zero_vector3, zero_vector3)

        cluster_i = cls._get_cluster(storage, clusters, start)
        cluster_j = cls._get_cluster(storage, clusters, stop)

        pose_i = create_vertex_i_with_status(Pose, storage, cluster_i, start, identity4x4)
        pose_j = create_vertex_j_with_status(storage, cluster_j, stop, pose_i)
        velocity_i = create_vertex_i_with_status(
            LinearVelocity, storage, cluster_i, start, zero_vector3
        )
        velocity_j = create_vertex_j_with_status(storage, cluster_j, stop, velocity_i)
        bias_i = create_vertex_i_with_status(ImuBias, storage, cluster_i, start, zero_bias)

        pim = get_integrated_measurement(
            cls._params, measurement, stop, cls.timescale_factor, bias_i.instance
        )

        edge = ImuOdometry(
            pose_i.instance,
            velocity_i.instance,
            bias_i.instance,
            pose_j.instance,
            velocity_j.instance,
            measurement,
            pim,
        )

        new_vertices = create_new_vertices([pose_i, velocity_i, bias_i, pose_j, velocity_j])

        table: dict[Vertex, int] = {
            pose_i.instance: start,
            velocity_i.instance: start,
            bias_i.instance: start,
            pose_j.instance: stop,
            velocity_j.instance: stop,
        }

        return GraphElement(edge, table, new_vertices)

    @classmethod
    def _get_cluster(
        cls, storage: VertexStorage, clusters: dict[VertexCluster, TimeRange], timestamp: int
    ) -> VertexCluster:
        """Gets a cluster in the storage or in clusters or creates a new one.

        Args:
            storage: a storage with clusters.

            clusters: clusters with the time ranges.

            timestamp: a timestamp of the cluster.

        Returns:
            cluster with vertices.
        """
        cluster = storage.get_cluster(timestamp)
        if cluster:
            return cluster

        cluster = get_cluster_for_timestamp_from_dict(clusters, timestamp)
        if cluster:
            return cluster

        cluster = get_cluster_for_timestamp_from_iterable(reversed(storage.clusters), timestamp)
        if cluster:
            return cluster

        return VertexCluster()
