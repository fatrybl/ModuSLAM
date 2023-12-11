from dataclasses import dataclass
from typing import Type

import gtsam

from slam.data_manager.factory.readers.element_factory import Element


@dataclass
class Edge:
    """
    Base Edge in Graph.
    """
    gtsam_factor: Type[gtsam.Factor]
    elements: tuple[Element, ...]
    vertex_1: int
    vertex_2: int | None = None


@dataclass
class LidarOdometry(Edge):
    """
    Lidar odometry based on scan matching.
    """
    gtsam_factor: gtsam.BetweenFactorPose3


@dataclass
class ImuOdometry(Edge):
    """
    Imu pre-integration.
    """
    gtsam_factor: gtsam.ImuFactor


@dataclass
class StereoCameraOdometry(Edge):
    """
    Stereo camera odometry based on images` features matching.
    """
    gtsam_factor: gtsam.BetweenFactorPose3
