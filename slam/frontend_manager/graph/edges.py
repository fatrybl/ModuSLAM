from dataclasses import dataclass
from typing import TypeVar

import gtsam

from slam.data_manager.factory.element import Element
from slam.frontend_manager.graph.vertices import Vertex


@dataclass
class Edge:
    """Base Edge of the Graph.

    Args:
        elements (tuple[Element, ...]): elements of DataBatch which create the edge.
        vertices (tuple[GraphVertex, ...]): vertices which are connected by the edge.
        factor (gtsam.Factor): factor from GTSAM library.
        noise_model (gtsam.noiseModel): noise model for the factor.
    """

    elements: tuple[Element, ...]
    vertices: tuple[Vertex, ...]
    factor: gtsam.Factor
    noise_model: gtsam.noiseModel


GraphEdge = TypeVar("GraphEdge", bound=Edge)


@dataclass
class Odometry(Edge):
    """Edge for any odometry factor."""

    vertex1: int
    vertex2: int


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
    factor: gtsam.SmartProjectionPose3Factor
