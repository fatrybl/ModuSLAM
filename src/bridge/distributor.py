"""Distributes measurement to the corresponding edges factory."""

import logging

from src.bridge.edge_factories.factory_protocol import EdgeFactory
from src.bridge.edge_factories.gps_position import Factory as GpsPositionFactory
from src.bridge.edge_factories.imu_bias import Factory as ImuBiasFactory
from src.bridge.edge_factories.imu_odometry.combined_odometry import (
    Factory as ImuOdometryFactory,
)
from src.bridge.edge_factories.linear_velocity import Factory as VelocityFactory
from src.bridge.edge_factories.pose import Factory as PoseFactory
from src.bridge.edge_factories.pose_odometry import Factory as PoseOdometryFactory
from src.bridge.edge_factories.split_pose_odometry import (
    Factory as SplitPoseOdometryFactory,
)
from src.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import ContinuousImu
from src.measurement_storage.measurements.imu_bias import Bias
from src.measurement_storage.measurements.linear_velocity import Velocity
from src.measurement_storage.measurements.pose import Pose
from src.measurement_storage.measurements.pose_odometry import OdometryWithElements
from src.measurement_storage.measurements.position import Position

logger = logging.getLogger(__name__)

# Add other measurement types and their corresponding factories here.
distribution_table: dict[type[Measurement], type[EdgeFactory]] = {
    OdometryWithElements: PoseOdometryFactory,
    SplitPoseOdometry: SplitPoseOdometryFactory,
    ContinuousImu: ImuOdometryFactory,
    Position: GpsPositionFactory,
    Pose: PoseFactory,
    Velocity: VelocityFactory,
    Bias: ImuBiasFactory,
}


def get_factory(measurement_type: type[Measurement]) -> EdgeFactory:
    """Returns an edge factory for the given measurement type if it has been defined.

    Args:
        measurement_type: a measurement type.

    Returns:
        edge factory.

    Raises:
        KeyError: if no edge factory has been defined for the given measurement type.
    """
    if measurement_type in distribution_table:
        return distribution_table[measurement_type]
    else:
        msg = f"No edge factory for the given measurement type{measurement_type} has been defined."
        logger.critical(msg)
        raise KeyError(msg)
