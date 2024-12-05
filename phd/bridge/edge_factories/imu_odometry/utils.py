import logging
from typing import Sequence, TypeVar

import gtsam
import numpy as np

from phd.logger.logging_config import frontend_manager
from phd.measurements.processed_measurements import (
    ContinuousImuMeasurement,
    ContinuousMeasurement,
    Imu,
)
from phd.moduslam.custom_types.numpy import Matrix3x3, Matrix4x4
from phd.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)

V = TypeVar("V", bound=Vertex)

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

    integrated_noise = pim.preintMeasCov()
    noise = gtsam.noiseModel.Gaussian.Covariance(integrated_noise)

    edge = ImuOdometry(pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j, measurement, noise)
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
        params: GTSAM integration parameters.

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


def integrate_measurements(
    pim: gtsam.PreintegratedCombinedMeasurements,
    measurements: Sequence[Imu],
    timestamp: int,
    time_scale: float,
) -> None:
    """Integrates the IMU measurements.

    Args:
        pim: gtsam pre-integrated measurement.

        measurements: IMU measurements sorted by timestamp.

        timestamp: integration time limit.

        time_scale: timescale factor.

    Raises:
        ValueError: if the measurements sequence is empty.
    """
    num_elements = len(measurements)

    if num_elements == 0:
        msg = "No measurements to integrate."
        logger.critical(msg)
        raise ValueError(msg)

    for i, measurement in enumerate(measurements):

        if i == num_elements - 1:
            dt = timestamp - measurement.timestamp

        else:
            dt = measurements[i + 1].timestamp - measurements[i].timestamp

        acc = np.array(measurement.acceleration)
        omega = np.array(measurement.angular_velocity)
        dt_secs = dt * time_scale

        pim.integrateMeasurement(acc, omega, dt_secs)


def get_integrated_measurement(
    integration_params: gtsam.PreintegrationCombinedParams,
    measurement: ContinuousImuMeasurement,
    timestamp: int,
    time_scale: float,
    bias: ImuBias,
) -> gtsam.PreintegratedCombinedMeasurements:
    """Integrates IMU measurements.

    Args:
        integration_params: GTSAM integration parameters.

        measurement: IMU measurement.

        timestamp: integration time limit.

        time_scale: timescale factor.

        bias: IMU bias.

    Returns:
        pre-integrated IMU measurement (gtsam.PreintegratedCombinedMeasurements).
    """
    first_m = measurement.items[0]
    accel_sample_covariance, ang_vel_sample_covariance = compute_covariance(measurement.items)
    tf = np.array(first_m.tf_base_sensor)
    integration_noise_covariance = np.array(first_m.integration_noise_covariance)
    accel_bias_covariance = np.array(first_m.accelerometer_bias_covariance)
    gyro_bias_covariance = np.array(first_m.gyroscope_bias_covariance)

    set_parameters(
        integration_params,
        tf,
        accel_sample_covariance,
        ang_vel_sample_covariance,
        integration_noise_covariance,
        accel_bias_covariance,
        gyro_bias_covariance,
    )
    pim = gtsam.PreintegratedCombinedMeasurements(integration_params)
    pim.resetIntegrationAndSetBias(bias.backend_instance)
    integrate_measurements(pim, measurement.items, timestamp, time_scale)
    return pim
