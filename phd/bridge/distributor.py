"""Distributes measurement to the corresponding edges factory."""

import logging

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.gps_position import Factory as GpsPositionFactory
from phd.bridge.edge_factories.imu_odometry.odometry import (
    Factory as ImuOdometryFactory,
)
from phd.bridge.edge_factories.linear_velocity import Factory as VelocityFactory
from phd.bridge.edge_factories.pose import Factory as PoseFactory
from phd.bridge.edge_factories.pose_odometry import Factory as PoseOdometryFactory
from phd.bridge.edge_factories.split_pose_odometry import (
    Factory as SplitPoseOdometryFactory,
)
from phd.measurements.auxiliary_classes import SplitPoseOdometry
from phd.measurements.processed import (
    ContinuousImuMeasurement,
    Gps,
    LinearVelocity,
    Measurement,
    Pose,
    PoseOdometry,
)

logger = logging.getLogger(__name__)

# Add other measurement types and their corresponding factories here.
distribution_table: dict[type[Measurement], type[EdgeFactory]] = {
    PoseOdometry: PoseOdometryFactory,
    SplitPoseOdometry: SplitPoseOdometryFactory,
    ContinuousImuMeasurement: ImuOdometryFactory,
    Gps: GpsPositionFactory,
    Pose: PoseFactory,
    LinearVelocity: VelocityFactory,
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
