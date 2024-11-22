from typing import TypeAlias

import gtsam
import numpy as np

from phd.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from phd.bridge.edge_factories.imu_odometry.utils import (
    compute_covariance,
    integrate,
    set_parameters,
)
from phd.bridge.edge_factories.utils import get_new_items
from phd.measurements.processed_measurements import ContinuousMeasurement, Imu
from phd.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
from phd.moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphElement,
    VerticesTable,
)
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

VerticesWithFlags: TypeAlias = tuple[
    tuple[Pose, bool], tuple[LinearVelocity, bool], tuple[ImuBias, bool]
]


class Factory(EdgeFactory):

    _gravity: float = 9.81
    _nanosecond: float = 1e-9
    _params = gtsam.PreintegrationCombinedParams.MakeSharedU(_gravity)

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: ContinuousMeasurement[Imu],
    ) -> GraphElement:
        """Creates a new ImuOdometry edge with preintegrated IMU factor.

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
        pose_j = cls._get_pose_j_with_status(storage, clusters, stop)
        velocity_j = cls._get_velocity_j_with_status(storage, clusters, stop)
        bias_j = cls._get_bias_j_with_status(storage, clusters, stop)

        pim = cls._integrate(measurement, stop, bias_i.instance)

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

        element = GraphElement(edge, new_vertices)
        return element

    @classmethod
    def _get_pose_i_with_status(
        cls,
        storage: VertexStorage,
        current_clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[Pose]:
        raise NotImplementedError

    @classmethod
    def _get_pose_j_with_status(
        cls,
        storage: VertexStorage,
        current_clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[Pose]:
        raise NotImplementedError

    @classmethod
    def _get_velocity_i_with_status(
        cls,
        storage: VertexStorage,
        current_clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[LinearVelocity]:
        raise NotImplementedError

    @classmethod
    def _get_velocity_j_with_status(
        cls,
        storage: VertexStorage,
        current_clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[LinearVelocity]:
        raise NotImplementedError

    @classmethod
    def _get_bias_i_with_status(
        cls,
        storage: VertexStorage,
        current_clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[ImuBias]:
        raise NotImplementedError

    @classmethod
    def _get_bias_j_with_status(
        cls,
        storage: VertexStorage,
        current_clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
    ) -> VertexWithStatus[ImuBias]:
        raise NotImplementedError

    @classmethod
    def _find_in_clusters(
        cls, current_clusters: dict[VertexCluster, TimeRange], timestamp: int
    ) -> VertexCluster | None:
        raise NotImplementedError

    @classmethod
    def _find_in_storage(cls, storage: VertexStorage, timestamp: int) -> VertexCluster | None:
        raise NotImplementedError

    @classmethod
    def _get_new_vertices(cls, vertices: list) -> VerticesTable:
        raise NotImplementedError

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
