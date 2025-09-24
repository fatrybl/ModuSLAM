import gtsam
from gtsam.noiseModel import Base

from moduslam.custom_types.aliases import Matrix4x4
from moduslam.frontend_manager.main_graph.edges.base import RadialEdge
from moduslam.frontend_manager.main_graph.vertices.custom import (
    Feature3D,
    Pose,
    identity4x4,
)
from moduslam.measurement_storage.measurements.visual_feature import Feature, Features


class SmartVisualFeature(RadialEdge):
    """Edge for SmartProjectionPose3Factor: https://dellaert.github.io/files/Carlone14icra.pdf"""

    def __init__(
        self,
        feature: Feature3D,
        noise_model: Base,
        camera_model: gtsam.gtsam.Cal3_S2,
        projection_params: gtsam.SmartProjectionParams,
        tf_base_sensor: Matrix4x4 = identity4x4,
    ) -> None:
        """
        Args:
            feature: a visual feature.

            noise_model: a GTSAM noise model for the factor (gtsam.noiseModel.Base).

            camera_model: a GTSAM camera model (gtsam.gtsam.Cal3_S2).

            tf_base_sensor: transformation matrix from base to sensor.

            projection_params: a GTSAM projection parameters (gtsam.SmartProjectionParams).
        """
        super().__init__()
        self._feature = feature
        self._poses: list[Pose] = []
        self._measurements: list[Feature] = []
        tf = gtsam.Pose3(tf_base_sensor)
        self._factor = gtsam.SmartProjectionPose3Factor(
            noise_model, camera_model, tf, projection_params
        )

    @property
    def factor(self) -> gtsam.SmartProjectionPose3Factor:
        """gtsam.SmartProjectionPose3Factor."""
        return self._factor

    @property
    def central_vertex(self) -> Feature3D:
        return self._feature

    @property
    def radial_vertices(self) -> list[Pose]:
        return self._poses

    @property
    def measurement(self) -> Features:
        raise NotImplementedError

    @property
    def vertices(self) -> list[Feature3D | Pose]:
        return [self._feature, *self._poses]

    def add_measurement(self, pose: Pose, measurement: Feature) -> None:
        """Adds a measurement of the feature from different pose.

        Args:
            pose: an observation pose.

            measurement: a new measurement of the same visual feature.
        """
        point = measurement.feature.key_point.pt
        self._factor.add(point, pose.backend_index)
        self._measurements.append(measurement)
        self._poses.append(pose)
