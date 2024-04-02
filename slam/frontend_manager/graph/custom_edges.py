import gtsam

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import (
    BinaryEdge,
    CalibrationEdge,
    MultiEdge,
)
from slam.frontend_manager.graph.base_vertices import GraphVertex


class SmartFactorEdge(CalibrationEdge):
    """Edge for Smart Factor in the Graph.

    Args:
        vertex (GraphVertex): main vertex.
        support_vertices (set[GraphVertex]): support vertices.
        measurements (tuple[Measurement, ...]): elements of DataBatch which create the edge.
        factor (gtsam.Factor): factor from GTSAM library.
        noise_model (gtsam.noiseModel): noise model for the factor.
    """

    def __init__(
        self,
        vertex: GraphVertex,
        support_vertices: set[GraphVertex],
        measurements: tuple[Measurement, ...],
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel,
    ) -> None:
        super().__init__(measurements, vertex, support_vertices, factor, noise_model)

    @property
    def all_vertices(self) -> set[GraphVertex]:
        return {self.vertex}.union(self.vertices)


class SmartStereoFeature(SmartFactorEdge):
    """
    Edge for smart Stereo Camera features:
        - https://dellaert.github.io/files/Carlone14icra.pdf
    TODO: check if a noise model is correct.
    """

    def __init__(
        self,
        vertex: GraphVertex,
        support_vertices: set[GraphVertex],
        measurements: tuple[Measurement, ...],
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel.Isotropic,
    ) -> None:
        super().__init__(vertex, support_vertices, measurements, factor, noise_model)

        self.K: gtsam.Cal3_S2 = gtsam.Cal3_S2()
        self.params: gtsam.SmartProjectionParams = gtsam.SmartProjectionParams()
        self.sensor_body: gtsam.Pose3 = gtsam.Pose3()


class ImuOdometry(MultiEdge):
    """Edge for Imu pre-integrated odometry."""


class LidarOdometry(BinaryEdge):
    """Edge for Lidar odometry."""


class StereoCameraOdometry(BinaryEdge):
    """Edge for Stereo Camera odometry."""
