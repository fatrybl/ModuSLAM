from typing import TypeAlias

import gtsam

from phd.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from phd.bridge.edge_factories.imu_odometry.utils import get_integrated_measurement
from phd.bridge.edge_factories.utils import (
    create_vertex,
    create_vertex_i_with_status,
    create_vertex_j_with_status,
    get_closest_cluster,
    get_cluster,
    get_new_items,
)
from phd.measurements.processed_measurements import ContinuousMeasurement, Imu
from phd.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity4x4, zero_vector3

VerticesWithFlags: TypeAlias = tuple[
    tuple[Pose, bool], tuple[LinearVelocity, bool], tuple[ImuBias, bool]
]


class Factory(EdgeFactory):

    timestamp_threshold_sec: float = 0.01
    timescale_factor: float = 1e-9
    _gravity: float = 9.81
    _params = gtsam.PreintegrationCombinedParams.MakeSharedU(_gravity)

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: ContinuousMeasurement[Imu],
    ) -> GraphElement:
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

        pose_i = cls._get_pose_i_with_status(storage, clusters, start)
        velocity_i = cls._get_velocity_i_with_status(storage, clusters, start)
        bias_i = cls._get_bias_i_with_status(storage, clusters, start)
        pose_j = cls._get_pose_j_with_status(storage, clusters, stop, pose_i)
        velocity_j = cls._get_velocity_j_with_status(storage, clusters, stop, velocity_i)
        bias_j = cls._get_bias_j_with_status(storage, clusters, stop, bias_i)

        pim = get_integrated_measurement(
            cls._params, measurement, stop, cls.timescale_factor, bias_i.instance
        )

        edge = ImuOdometry(
            pose_i.instance,
            velocity_i.instance,
            bias_i.instance,
            pose_j.instance,
            velocity_j.instance,
            bias_j.instance,
            measurement,
            pim,
        )

        new_vertices = get_new_items([pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j])

        return GraphElement(edge, new_vertices)

    @classmethod
    def _get_pose_i_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[Pose]:
        """Gets i-th (previous) pose with the status.

        Args:
            storage: global storage with clusters.

            clusters: clusters with the time ranges.

            timestamp: timestamp of the i-th pose.

        Returns:
            pose with the status.
        """

        cluster = storage.get_cluster(timestamp)
        if cluster:
            item = create_vertex_i_with_status(Pose, storage, cluster, timestamp, identity4x4)
            return item

        cluster = get_cluster(clusters, timestamp)
        if cluster:
            item = create_vertex_i_with_status(Pose, storage, cluster, timestamp, identity4x4)
            return item

        cluster = get_closest_cluster(storage, timestamp, cls.timestamp_threshold_sec)
        if cluster:
            item = create_vertex_i_with_status(Pose, storage, cluster, timestamp, identity4x4)
            return item

        cluster = VertexCluster()
        pose = create_vertex(Pose, storage, identity4x4)
        return VertexWithStatus(pose, cluster=cluster, is_new=True, timestamp=timestamp)

    @classmethod
    def _get_pose_j_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
        pose_i: VertexWithStatus[Pose],
    ) -> VertexWithStatus[Pose]:
        """Gets j-th pose (current) with the status.

        Args:
            storage: global storage with vertices.

            clusters: clusters with the time ranges.

            timestamp: timestamp of the j-th pose.

            pose_i: previous pose.

        Returns:
            pose with status.
        """
        cluster = get_cluster(clusters, timestamp)
        item = create_vertex_j_with_status(storage, cluster, timestamp, pose_i)
        return item

    @classmethod
    def _get_velocity_i_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[LinearVelocity]:
        """Gets i-th velocity with the status.

        Args:
            storage: a storage with vertices.

            clusters: clusters with the time ranges.

            timestamp: timestamp of the i-th velocity.

        Returns:
            velocity with the status.
        """
        cluster = storage.get_cluster(timestamp)
        if cluster:
            item = create_vertex_i_with_status(
                LinearVelocity, storage, cluster, timestamp, zero_vector3
            )
            return item

        cluster = get_cluster(clusters, timestamp)
        if cluster:
            item = create_vertex_i_with_status(
                LinearVelocity, storage, cluster, timestamp, zero_vector3
            )
            return item

        cluster = get_closest_cluster(storage, timestamp, cls.timestamp_threshold_sec)
        if cluster:
            item = create_vertex_i_with_status(
                LinearVelocity, storage, cluster, timestamp, zero_vector3
            )
            return item

        cluster = VertexCluster()
        default = (0, 0, 0)
        velocity = create_vertex(LinearVelocity, storage, default)
        return VertexWithStatus(velocity, cluster=cluster, is_new=True, timestamp=timestamp)

    @classmethod
    def _get_velocity_j_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
        velocity_i: VertexWithStatus[LinearVelocity],
    ) -> VertexWithStatus[LinearVelocity]:
        """Gets j-th velocity (current) with the status.

        Args:
            storage: global storage with vertices.

            clusters: clusters with the time ranges.

            timestamp: timestamp of the j-th pose.

            velocity_i: previous velocity

        Returns:
            velocity with status.
        """
        cluster = get_cluster(clusters, timestamp)
        item = create_vertex_j_with_status(storage, cluster, timestamp, velocity_i)
        return item

    @classmethod
    def _get_bias_i_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[ImuBias]:
        """Gets i-th (previous) imu bias with the status.

        Args:
            storage: global storage with clusters.

            clusters: clusters with the time ranges.

            timestamp: timestamp of the i-th pose.

        Returns:
            imu bias with status.
        """
        zero_bias = (zero_vector3, zero_vector3)
        cluster = storage.get_cluster(timestamp)

        if cluster:
            item = create_vertex_i_with_status(ImuBias, storage, cluster, timestamp, zero_bias)
            return item

        cluster = get_cluster(clusters, timestamp)
        if cluster:
            item = create_vertex_i_with_status(ImuBias, storage, cluster, timestamp, zero_bias)
            return item

        cluster = get_closest_cluster(storage, timestamp, cls.timestamp_threshold_sec)
        if cluster:
            item = create_vertex_i_with_status(ImuBias, storage, cluster, timestamp, zero_bias)
            return item

        cluster = VertexCluster()
        bias = create_vertex(ImuBias, storage, zero_bias)
        return VertexWithStatus(bias, cluster=cluster, is_new=True, timestamp=timestamp)

    @classmethod
    def _get_bias_j_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
        bias_i: VertexWithStatus[ImuBias],
    ) -> VertexWithStatus[ImuBias]:
        """Gets j-th bias (current) with the status.

        Args:
            storage: global storage with vertices.

            clusters: clusters with the time ranges.

            timestamp: timestamp of the j-th pose.

            bias_i: previous bias.

        Returns:
            bias with status.
        """
        cluster = get_cluster(clusters, timestamp)
        item = create_vertex_j_with_status(storage, cluster, timestamp, bias_i)
        return item
