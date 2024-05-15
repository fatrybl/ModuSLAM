from collections.abc import Iterable

import gtsam
import numpy as np

from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.custom_edges import ImuOdometry
from slam.frontend_manager.graph.custom_vertices import ImuBias, Pose, Velocity
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.frontend_manager.handlers.imu_data_preprocessor import ImuData
from slam.frontend_manager.measurement_storage import Measurement
from slam.utils.numpy_types import Matrix3x3, Matrix4x4
from slam.utils.ordered_set import OrderedSet


def create_vertex(vertex_type: type[GraphVertex], index: int, timestamp: int) -> GraphVertex:
    """Creates the graph vertex.

    Args:
        vertex_type: type of the vertex.

        index: index of the vertex.

        timestamp: timestamp of the vertex.

    Returns:
        new vertex.
    """
    vertex = vertex_type()
    vertex.index = index
    vertex.timestamp = timestamp
    return vertex


def get_previous_vertex(
    vertex_type: type[GraphVertex],
    storage: VertexStorage,
    timestamp: int,
    index: int,
    time_margin: float,
) -> GraphVertex:
    """Gets previous vertex if found or creates a new one.

    Args:
        vertex_type: type of the vertex.

        storage: storage of vertices.

        timestamp: timestamp of the vertex.

        index: index of the vertex.

        time_margin: time margin for searching the closest vertex.

    Returns:
        vertex.
    """

    vertex = storage.get_last_vertex(vertex_type)
    if vertex and vertex.timestamp == timestamp:
        return vertex

    vertex = storage.find_closest_optimizable_vertex(vertex_type, timestamp, time_margin)
    if vertex:
        return vertex
    else:
        new_index = index + 1
        new_vertex: GraphVertex = create_vertex(
            vertex_type=vertex_type, index=new_index, timestamp=timestamp
        )
        return new_vertex


def create_edge(
    pose_i: Pose,
    velocity_i: Velocity,
    bias_i: ImuBias,
    pose_j: Pose,
    velocity_j: Velocity,
    bias_j: ImuBias,
    measurements: tuple[Measurement, ...],
    pim: gtsam.PreintegratedCombinedMeasurements,
) -> ImuOdometry:
    """Creates new edge of type ImuOdometry.

    Returns:
        new edge.
    """

    factor = gtsam.CombinedImuFactor(
        pose_i.gtsam_index,
        velocity_i.gtsam_index,
        pose_j.gtsam_index,
        velocity_j.gtsam_index,
        bias_i.gtsam_index,
        bias_j.gtsam_index,
        pim,
    )

    integrated_noise = pim.preintMeasCov()
    noise = gtsam.noiseModel.Gaussian.Covariance(integrated_noise)

    edge = ImuOdometry(
        vertex_set_1={pose_i, velocity_i, bias_i},
        vertex_set_2={pose_j, velocity_j, bias_j},
        measurements=measurements,
        factor=factor,
        noise_model=noise,
    )
    return edge


def compute_covariance(measurements: Iterable[Measurement]):
    accelerations = [m.values.acceleration for m in measurements]
    angular_velocities = [m.values.angular_velocity for m in measurements]
    acc_cov = np.cov(accelerations, rowvar=False)
    gyro_cov = np.cov(angular_velocities, rowvar=False)
    return acc_cov, gyro_cov


def set_parameters(
    params: gtsam.PreintegrationCombinedParams,
    tf_base_sensor: Matrix4x4,
    acc_cov: Matrix3x3,
    gyro_cov: Matrix3x3,
    integration_cov: Matrix3x3,
    bias_acc_cov: Matrix3x3,
    bias_omega_cov: Matrix3x3,
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

    measurements_list = list(measurements)
    num_elements = len(measurements_list)

    for idx, m in enumerate(measurements):

        if idx == num_elements - 1:
            dt_nanoseconds = timestamp - measurements.last.time_range.start

        else:
            dt_nanoseconds = measurements_list[idx + 1].time_range.start - m.time_range.start

        values: ImuData = m.values
        acc = values.acceleration
        omega = values.angular_velocity

        dt_secs: float = dt_nanoseconds * time_scale
        pim.integrateMeasurement(acc, omega, dt_secs)

    return pim
