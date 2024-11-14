import logging
from typing import Sequence

import gtsam
import numpy as np

from phd.logger.logging_config import frontend_manager
from phd.measurements.processed_measurements import ContinuousMeasurement, Imu
from phd.moduslam.custom_types.numpy import Matrix3x3, Matrix4x4
from phd.moduslam.frontend_manager.main_graph.edges.custom import ImuOdometry
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)

logger = logging.getLogger(frontend_manager)


def create_edge(
    pose_i: Pose,
    velocity_i: LinearVelocity,
    bias_i: ImuBias,
    pose_j: Pose,
    velocity_j: LinearVelocity,
    bias_j: ImuBias,
    measurement: ContinuousMeasurement,
    pim: gtsam.PreintegratedCombinedMeasurements,
) -> ImuOdometry:
    """Creates new edge of type ImuOdometry."""

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
        pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j, measurement, factor, noise
    )
    return edge


def compute_covariance(
    measurements: Sequence[Imu],
) -> tuple[Matrix3x3, Matrix3x3]:
    """Computes the covariance of the accelerometer and gyroscope measurements [x,y,z].
    If only one measurement is available, the default covariance is used.

    Args:
        measurements: IMU measurements.

    Returns:
        accelerometer and gyroscope noise covariance matrices.

    Raises:
        ValueError: if the measurements sequence is empty.
    """
    if len(measurements) == 0:
        msg = "Empty measurements sequence."
        logger.critical(msg)
        raise ValueError(msg)

    elif len(measurements) == 1:
        acc_cov = np.array(measurements[0].acceleration_covariance)
        gyro_cov = np.array(measurements[0].angular_velocity_covariance)

    else:
        accelerations = np.array([m.acceleration for m in measurements])
        angular_velocities = np.array([m.angular_velocity for m in measurements])

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
    measurements: Sequence[Imu],
    timestamp: int,
    time_scale: float,
) -> gtsam.PreintegratedCombinedMeasurements:
    """Integrates the IMU measurements.

    Args:
        pim: gtsam preintegrated measurement instance.

        measurements: IMU measurements sorted by timestamp.

        timestamp: integration time limit.

        time_scale: timescale factor.

    Returns:
        integrated IMU measurements.

    Raises:
        ValueError: if the measurements sequence is empty.

    TODO: check if the integration process is correct: dt is computed properly.
    """
    num_elements = len(measurements)

    if num_elements == 0:
        msg = "No measurements to integrate."
        logger.critical(msg)
        raise ValueError(msg)

    for idx, measurement in enumerate(measurements):

        if idx == num_elements - 1:
            dt_nanosec = timestamp - measurement.timestamp

        else:
            dt_nanosec = measurements[idx + 1].timestamp - measurements[idx].timestamp

        acc = np.array(measurement.acceleration)
        omega = np.array(measurement.angular_velocity)
        dt_secs = dt_nanosec * time_scale

        pim.integrateMeasurement(acc, omega, dt_secs)

    return pim
