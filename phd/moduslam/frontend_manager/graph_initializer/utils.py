from typing import cast

import gtsam

from phd.measurements.processed import ImuBias, LinearVelocity, Pose
from phd.moduslam.custom_types.aliases import Matrix4x4, Vector6
from phd.moduslam.frontend_manager.graph_initializer.config_objects import (
    PriorImuBias,
    PriorLinearVelocity,
    PriorPose,
)
from phd.moduslam.utils.auxiliary_methods import diagonal_matrix3x3


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
    se3_pose = pose_se3_from_tuple(config.measurement)
    position_covariance = diagonal_matrix3x3(config.noise_covariance[:3])
    orientation_covariance = diagonal_matrix3x3(config.noise_covariance[3:])
    return Pose(config.timestamp, se3_pose, position_covariance, orientation_covariance, [])


def create_linear_velocity(config: PriorLinearVelocity) -> LinearVelocity:
    """Creates a linear velocity measurement from the given config.

    Args:
        config: a configuration to create a measurement from.

    Returns:
        a linear velocity measurement.
    """
    covariance_matrix = diagonal_matrix3x3(config.noise_covariance)
    return LinearVelocity(config.timestamp, config.measurement, covariance_matrix, [])


def create_imu_bias(config: PriorImuBias) -> ImuBias:
    """Creates an imu bias measurement from the given config.

    Args:
        config: a configuration to create a measurement from.

    Returns:
        an imu bias measurement.
    """
    accel_bias_covariance_matrix = diagonal_matrix3x3(config.noise_covariance[:3])
    vel_bias_covariance_matrix = diagonal_matrix3x3(config.noise_covariance[3:])
    return ImuBias(
        config.timestamp,
        config.measurement[:3],
        config.measurement[3:],
        accel_bias_covariance_matrix,
        vel_bias_covariance_matrix,
        [],
    )
