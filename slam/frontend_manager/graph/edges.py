from dataclasses import dataclass
from typing import TypeVar

import gtsam

from slam.data_manager.factory.element import Element
from slam.frontend_manager.graph.vertices import Vertex


@dataclass
class Edge:
    """Base Edge of the Graph.

    Args:
        id (int): unique id of the edge.
        elements (tuple[Element, ...]): elements of DataBatch which create the edge.
        vertices (tuple[Vertex, ...]): vertices which are connected by the edge.
        gtsam_factor (gtsam.Factor): factor from GTSAM library.
    """

    id: int
    elements: tuple[Element, ...]
    vertices: tuple[Vertex, ...]
    gtsam_factor: gtsam.Factor
    noise_model: gtsam.noiseModel


GraphEdge = TypeVar("GraphEdge", bound=Edge)


@dataclass
class Odometry(Edge):
    """Edge for any odometry factor."""

    v1: int
    v2: int


@dataclass
class ImuOdometry(Odometry):
    """Edge for Imu pre-integrated odometry."""


@dataclass
class LidarOdometry(Odometry):
    """Edge for Lidar odometry."""


@dataclass
class StereoCameraOdometry(Odometry):
    """Edge for Stereo Camera odometry."""


@dataclass
class SmartStereoLandmark(Edge):
    """
    Edge for smart Stereo Camera landmarks:
        - https://dellaert.github.io/files/Carlone14icra.pdf
    TODO: check if a model is correct.
    """

    noise_model: gtsam.noiseModel.Isotropic
    K: gtsam.Cal3_S2
    params: gtsam.SmartProjectionParams
    sensor_body: gtsam.Pose3
    gtsam_factor: gtsam.SmartProjectionPose3Factor
