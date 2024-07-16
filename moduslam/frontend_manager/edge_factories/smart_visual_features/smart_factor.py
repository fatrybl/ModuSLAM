import gtsam

from moduslam.utils.numpy_types import Matrix3x3, Matrix4x4


class VisualSmartFactorFactory:
    def __init__(self, smart_projection_params: dict[str, bool] | None = None):
        """
        Args:
            smart_projection_params: parameters of GTSAM SmartProjectionParams instance.
        """
        self._projection_params = gtsam.SmartProjectionParams()

    def create(
        self,
        tf_base_camera: Matrix4x4,
        camera_matrix: Matrix3x3,
        noise_model: gtsam.noiseModel.Diagonal.Covariance,
    ) -> gtsam.SmartProjectionPose3Factor:
        """Creates a GTSAM SmartProjectionPose3 factor.

        Args:
            tf_base_camera: GTSAM transformation from the base to the camera.

            camera_matrix: 3x3 camera matrix.

            noise_model: GTSAM noise model.

        Returns:
            GTSAM smart projection factor.
        """
        tf = gtsam.Pose3(tf_base_camera)
        fx, fy, cx, cy = (
            camera_matrix[0, 0],
            camera_matrix[1, 1],
            camera_matrix[0, 2],
            camera_matrix[1, 2],
        )
        s = 0.0
        matrix = gtsam.Cal3_S2(fx, fy, s, cx, cy)
        factor = gtsam.SmartProjectionPose3Factor(noise_model, matrix, tf, self._projection_params)
        return factor
