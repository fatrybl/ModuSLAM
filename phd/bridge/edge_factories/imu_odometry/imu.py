from typing import TypeAlias

import gtsam
import numpy as np

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.imu_odometry.utils import (
    compute_covariance,
    create_edge,
    integrate,
    set_parameters,
)
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.measurements.processed_measurements import ContinuousMeasurement, Imu
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import (
    GraphElement,
    VertexWithTimestamp,
    VerticesTable,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)

VerticesWithFlags: TypeAlias = tuple[
    tuple[Pose, bool], tuple[LinearVelocity, bool], tuple[ImuBias, bool]
]


class Factory(EdgeFactory):

    _gravity: float = 9.81
    _nanosecond: float = 1e-9
    _params = gtsam.PreintegrationCombinedParams.MakeSharedU(_gravity)

    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement: ContinuousMeasurement[Imu]
    ) -> GraphElement:
        """Creates a new ImuOdometry edge with IMU factor.

        Args:
            graph: a main graph.

            cluster: a common cluster for new vertices.

            measurement: an IMU measurement.

        Returns:
            new element.
        """
        start = measurement.time_range.start
        stop = measurement.time_range.stop

        pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j, new_vertices = cls._get_vertices(
            graph, cluster, start, stop
        )

        pim = cls._integrate(measurement, stop, bias_i)

        edge = create_edge(pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j, measurement, pim)

        element = GraphElement(edge, new_vertices)

        return element

    @classmethod
    def _get_vertices(
        cls, graph: Graph, cluster: VertexCluster, start: int, stop: int
    ) -> tuple[Pose, LinearVelocity, ImuBias, Pose, LinearVelocity, ImuBias, VerticesTable]:
        cluster_i = graph.vertex_storage.get_cluster(start)
        cluster_j = cluster

        if cluster_i:
            vertices_i_table = cls._process_cluster(graph, cluster_i)
        else:
            cluster_i = VertexCluster()
            pose_i, velocity_i, bias_i = cls._create_new_vertices(graph)
            vertices_i_table = ((pose_i, True), (velocity_i, True), (bias_i, True))

        vertices_j_table = cls._process_cluster(graph, cluster_j)

        table_i = cls._create_table(cluster_i, vertices_i_table, start)
        table_j = cls._create_table(cluster_j, vertices_j_table, stop)
        new_vertices = table_i | table_j

        pose_i, velocity_i, bias_i = cls._get_pose_velocity_bias(vertices_i_table)
        pose_j, velocity_j, bias_j = cls._get_pose_velocity_bias(vertices_j_table)

        return pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j, new_vertices

    @classmethod
    def _integrate(
        cls, measurement: ContinuousMeasurement[Imu], timestamp: int, bias: ImuBias
    ) -> gtsam.PreintegratedImuMeasurements:
        """Integrates IMU measurements.

        Args:
            measurement: an IMU measurement.

            timestamp: an integration time limit.

            bias: IMU bias.

        Returns:
            pre-integrated IMU measurement (gtsam instance).
        """
        first_m = measurement.items[0]
        accel_sample_covariance, ang_vel_sample_covariance = compute_covariance(measurement.items)
        tf = np.array(first_m.tf_base_sensor)
        integration_noise_covariance = np.array(first_m.integration_noise_covariance)
        accel_bias_covariance = np.array(first_m.accelerometer_bias_covariance)
        gyro_bias_covariance = np.array(first_m.gyroscope_bias_covariance)

        set_parameters(
            cls._params,
            tf,
            accel_sample_covariance,
            ang_vel_sample_covariance,
            integration_noise_covariance,
            accel_bias_covariance,
            gyro_bias_covariance,
        )
        pim = gtsam.PreintegratedImuMeasurements(cls._params)
        pim.resetIntegrationAndSetBias(bias)
        pim = integrate(pim, measurement.items, timestamp, cls._nanosecond)
        return pim

    @classmethod
    def _create_new_vertices(cls, graph: Graph) -> tuple[Pose, LinearVelocity, ImuBias]:
        """Creates new vertices for IMU odometry edge.

        Args:
            graph: a main graph.

        Returns:
            pose, velocity, bias.
        """
        pose = create_new_vertex(Pose, graph)
        velocity = create_new_vertex(LinearVelocity, graph)
        bias = create_new_vertex(ImuBias, graph)
        return pose, velocity, bias

    @staticmethod
    def _create_table(
        cluster, vertices: VerticesWithFlags, timestamp: int
    ) -> dict[VertexCluster, list[VertexWithTimestamp]]:
        """Creates a table of cluster and vertices with the timestamp.

        Args:
            cluster: a cluster.

            vertices: vertices with boolean flags.

            timestamp: a timestamp.

        Returns:
            a table of cluster and vertices with the timestamp.
        """
        table: dict[VertexCluster, list[VertexWithTimestamp]] = {}
        for vertex, flag in vertices:
            if flag:
                table[cluster].append((vertex, timestamp))
        return table

    @staticmethod
    def _get_pose_velocity_bias(table: VerticesWithFlags) -> tuple[Pose, LinearVelocity, ImuBias]:
        """Gets pose, velocity, bias from the table.

        Args:
            table: vertices with boolean flags.

        Returns:
            pose, velocity, bias.
        """
        pose_i, velocity_i, bias_i = table[0][0], table[1][0], table[2][0]
        return pose_i, velocity_i, bias_i

    @staticmethod
    def _process_cluster(graph: Graph, cluster: VertexCluster) -> VerticesWithFlags:
        """Creates new vertices or retrieves existing ones from the cluster. If a new
        vertex is created, the flag is set to True.

        Args:
            graph: a main graph.

            cluster: a cluster with vertices.

        Returns:
            a table of vertices with boolean flags.
        """

        new_pose, new_velocity, new_bias = False, False, False

        pose = cluster.get_latest_vertex(Pose)
        velocity = cluster.get_latest_vertex(LinearVelocity)
        bias = cluster.get_latest_vertex(ImuBias)

        if pose:
            pose_i = pose
        else:
            new_pose = True
            pose_i = create_new_vertex(Pose, graph)

        if velocity:
            velocity_i = velocity
        else:
            new_velocity = True
            velocity_i = create_new_vertex(LinearVelocity, graph)

        if bias:
            bias_i = bias
        else:
            new_bias = True
            bias_i = create_new_vertex(ImuBias, graph)

        vertex_table = (pose_i, new_pose), (velocity_i, new_velocity), (bias_i, new_bias)
        return vertex_table
