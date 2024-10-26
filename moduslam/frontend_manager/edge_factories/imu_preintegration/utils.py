import logging
from collections import OrderedDict
from collections.abc import Iterable
from typing import Any

import gtsam
import numpy as np

from moduslam.custom_types.aliases import Matrix4x4, Vector3
from moduslam.custom_types.numpy import Matrix3x3 as NumpyMatrix3x3
from moduslam.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from moduslam.frontend_manager.edge_factories.utils import get_last_vertex
from moduslam.frontend_manager.graph.base_vertices import BaseVertex
from moduslam.frontend_manager.graph.custom_edges import ImuOdometry
from moduslam.frontend_manager.graph.custom_vertices import (
    ImuBias,
    LinearVelocity,
    Pose,
)
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.frontend_manager.handlers.imu_data_preprocessor.line_parsers import (
    ImuData,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


def create_vertex(
    vertex_type: type[BaseVertex], index: int, timestamp: int, value: Any
) -> BaseVertex:
    return vertex_type(index, timestamp, value)


def create_edge(
    pose_i: Pose,
    velocity_i: LinearVelocity,
    bias_i: ImuBias,
    pose_j: Pose,
    velocity_j: LinearVelocity,
    bias_j: ImuBias,
    measurements: list[Measurement],
    pim: gtsam.PreintegratedCombinedMeasurements,
) -> ImuOdometry:
    """Creates new edge of type ImuOdometry.

    Returns:
        new edge.
    """

    factor = gtsam.CombinedImuFactor(
        pose_i.backend_index,
        velocity_i.backend_index,
        pose_j.backend_index,
        velocity_j.backend_index,
        bias_i.backend_index,
        bias_j.backend_index,
        pim,
    )

    integrated_noise = pim.preintMeasCov()
    noise = gtsam.noiseModel.Gaussian.Covariance(integrated_noise)

    edge = ImuOdometry(
        vertices=[pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j],
        measurements=measurements,
        factor=factor,
        noise_model=noise,
    )
    return edge


def compute_covariance(
    measurements: Iterable[Measurement],
) -> tuple[NumpyMatrix3x3, NumpyMatrix3x3]:
    """Computes the covariance of the accelerometer and gyroscope measurements [x,y,z].
    If only one measurement is available, the default covariance is used.

    Args:
        measurements: IMU measurements.

    Returns:
        accelerometer and gyroscope noise covariance matrices.
    """

    accelerations = np.array([m.value.acceleration for m in measurements], dtype=np.float64)
    angular_velocities = np.array(
        [m.value.angular_velocity for m in measurements], dtype=np.float64
    )

    acc_cov = np.cov(accelerations, rowvar=False)
    gyro_cov = np.cov(angular_velocities, rowvar=False)

    return acc_cov, gyro_cov


def set_parameters(
    params: gtsam.PreintegrationCombinedParams,
    tf_base_sensor: NumpyMatrix4x4,
    acc_cov: NumpyMatrix3x3,
    gyro_cov: NumpyMatrix3x3,
    integration_cov: NumpyMatrix3x3,
    bias_acc_cov: NumpyMatrix3x3,
    bias_omega_cov: NumpyMatrix3x3,
) -> None:
    """Sets the parameters for the IMU measurements preintegration.

    Args:
        params: preintegration parameters.

        tf_base_sensor: transformation matrix from base to sensor frame.

        acc_cov: accelerometer noise covariance.

        gyro_cov: gyroscope noise covariance.

        integration_cov: integration noise covariance.

        bias_acc_cov: accelerometer bias noise covariance.

        bias_omega_cov: gyroscope bias noise covariance.
    """
    params.setBodyPSensor(gtsam.Pose3(tf_base_sensor))
    params.setAccelerometerCovariance(acc_cov)
    params.setGyroscopeCovariance(gyro_cov)
    params.setIntegrationCovariance(integration_cov)
    params.setBiasAccCovariance(bias_acc_cov)
    params.setBiasOmegaCovariance(bias_omega_cov)


def integrate(
    pim: gtsam.PreintegratedCombinedMeasurements,
    measurements: OrderedSet[Measurement],
    timestamp: int,
    time_scale: float,
) -> gtsam.PreintegratedCombinedMeasurements:
    """Integrates the IMU measurements.

    Args:
        pim: gtsam preintegrated measurements.

        measurements: IMU measurements.

        timestamp: integration time limit.

        time_scale: timescale factor.

    Returns:
        preintegrated IMU measurements.
    """

    if len(measurements) == 0:
        msg = "No measurements to integrate."
        logger.critical(msg)
        raise ValueError(msg)

    measurements_list = list(measurements)
    num_elements = len(measurements_list)

    for idx, measurement in enumerate(measurements):

        if idx == num_elements - 1:
            dt_nanoseconds = timestamp - measurements.last.time_range.start

        else:
            dt_nanoseconds = (
                measurements_list[idx + 1].time_range.start - measurement.time_range.start
            )

        if dt_nanoseconds <= 0:
            msg = "dt <= 0. Stopping integration of IMU measurements."
            logger.error(msg)
            return pim

        values: ImuData = measurement.value
        acc = np.array(values.acceleration)
        omega = np.array(values.angular_velocity)

        dt_secs = dt_nanoseconds * time_scale
        pim.integrateMeasurement(acc, omega, dt_secs)

    return pim


def get_vertices(
    storage: VertexStorage,
    timestamp: int,
    time_margin: int,
    index: int | None = None,
    default_values: tuple[Matrix4x4, Vector3, tuple[Vector3, Vector3]] | None = None,
) -> tuple[Pose, LinearVelocity, ImuBias, bool]:
    """Gets the vertices from the storage or creates new ones.

    Args:
        storage: storage with vertices.

        timestamp: timestamp.

        time_margin: time margin.

        index: indices of the vertices (optional).

        default_values: default values for the vertices (optional).

    Returns:
        vertices and new index flag.
    """
    is_new_index = False

    pose = get_last_vertex(Pose, storage, timestamp, time_margin)
    velocity = get_last_vertex(LinearVelocity, storage, timestamp, time_margin)
    bias = get_last_vertex(ImuBias, storage, timestamp, time_margin)

    if pose and velocity and bias:
        return pose, velocity, bias, is_new_index

    elif pose is None and velocity is None and bias is None:
        if index is not None:
            new_index = index
        else:
            new_index = generate_index(storage.index_storage)
            is_new_index = True

        if default_values:
            default_pose = default_values[0]
            default_velocity = default_values[1]
            default_bias = default_values[2]
            pose = Pose(index=new_index, timestamp=timestamp, value=default_pose)
            velocity = LinearVelocity(index=new_index, timestamp=timestamp, value=default_velocity)
            bias = ImuBias(index=new_index, timestamp=timestamp, value=default_bias)
        else:
            pose = Pose(index=new_index, timestamp=timestamp)
            velocity = LinearVelocity(index=new_index, timestamp=timestamp)
            bias = ImuBias(index=new_index, timestamp=timestamp)

    else:
        vertices = (pose, velocity, bias)
        pose, velocity, bias = create_missing_vertices(vertices)

    return pose, velocity, bias, is_new_index


def create_missing_vertices(
    vertices: tuple[Pose | LinearVelocity | ImuBias | None, ...]
) -> tuple[Pose, LinearVelocity, ImuBias]:
    """Creates missing vertices.

    Args:
        vertices: vertices to be checked.

    Returns:
        new vertices.
    """
    type_vertex_table = OrderedDict({type(v): v for v in vertices if v is not None})

    if not type_vertex_table:
        msg = "All vertices are None"
        logger.critical(msg)
        raise ValueError(msg)

    existing_vertex = next(iter(type_vertex_table.values()))
    index = existing_vertex.index
    timestamp = existing_vertex.timestamp

    new_vertices = []
    for v_type in [Pose, LinearVelocity, ImuBias]:
        if v_type not in type_vertex_table:
            vertex = v_type(index=index, timestamp=timestamp)  # type: ignore

        else:
            vertex = type_vertex_table[v_type]  # type: ignore

        new_vertices.append(vertex)

    return tuple(new_vertices)  # type: ignore
