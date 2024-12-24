from typing import cast

import gtsam

from phd.measurement_storage.measurements.imu_bias import Bias
from phd.measurement_storage.measurements.linear_velocity import Velocity
from phd.measurement_storage.measurements.pose import Pose
from phd.moduslam.custom_types.aliases import Matrix4x4, Vector6
from phd.moduslam.frontend_manager.graph_initializer.configs import (
    PriorImuBias,
    PriorLinearVelocity,
    PriorPose,
)
from phd.utils.auxiliary_methods import diagonal_matrix3x3


def pose_se3_from_tuple(values: Vector6) -> Matrix4x4:
    """Creates a pose SE(3) matrix from the vector.

    Args:
        values: [x, y, z, yaw, pitch, roll] vector.

    Returns:
        a pose SE(3) matrix.
    """
    trans = values[:3]
    rot = gtsam.Rot3.Ypr(*values[3:])
    pose_numpy = gtsam.Pose3(rot, trans).matrix()
    pose_tuple = tuple(map(tuple, pose_numpy))
    pose = cast(Matrix4x4, pose_tuple)
    return pose


def create_pose(config: PriorPose) -> Pose:
    """Creates a pose measurement from the given config.

    Args:
        config: a configuration to create a measurement from.

    Returns:
        a pose measurement.
    """
    cov = config.noise_covariance
    se3_pose = pose_se3_from_tuple(config.measurement)
    position_covariance = diagonal_matrix3x3((cov[0], cov[1], cov[2]))
    orientation_covariance = diagonal_matrix3x3((cov[3], cov[4], cov[5]))
    return Pose(config.timestamp, se3_pose, position_covariance, orientation_covariance)


def create_linear_velocity(config: PriorLinearVelocity) -> Velocity:
    """Creates a linear velocity measurement from the given config.

    Args:
        config: a configuration to create a measurement from.

    Returns:
        a linear velocity measurement.
    """
    covariance_matrix = diagonal_matrix3x3(config.noise_covariance)
    return Velocity(config.timestamp, config.measurement, covariance_matrix)


def create_imu_bias(config: PriorImuBias) -> Bias:
    """Creates an imu bias measurement from the given config.

    Args:
        config: a configuration to create a measurement from.

    Returns:
        an imu bias measurement.
    """
    m = config.measurement
    cov = config.noise_covariance
    acceleration = (m[0], m[1], m[2])
    velocity = (m[3], m[4], m[5])
    accel_bias_covariance_matrix = diagonal_matrix3x3((cov[0], cov[1], cov[2]))
    vel_bias_covariance_matrix = diagonal_matrix3x3((cov[3], cov[4], cov[5]))

    return Bias(
        config.timestamp,
        acceleration,
        velocity,
        accel_bias_covariance_matrix,
        vel_bias_covariance_matrix,
    )
