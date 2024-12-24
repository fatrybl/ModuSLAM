import logging

import numpy as np
from kiss_icp.kiss_icp import KISSConfig, KissICP

from phd.external.handlers_factory.handlers.handler_protocol import Handler
from phd.external.handlers_factory.handlers.scan_matcher.config import (
    KissIcpScanMatcherConfig,
)
from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.measurements.pose_odometry import OdometryWithElements
from phd.moduslam.custom_types.aliases import Matrix3x3, Matrix4x4
from phd.moduslam.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.utils import create_empty_element
from phd.moduslam.sensors_factory.sensors import Lidar3D
from phd.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(frontend_manager)


class ScanMatcher(Handler):
    """
    Handler computes the transformation between two point clouds based on Kiss-ICP method:
    https://github.com/PRBonn/kiss-icp.
    """

    _elements_queue_size: int = 2  # number of elements to compute the transformation
    _num_channels: int = 4  # x, y, z, intensity

    def __init__(self, config: KissIcpScanMatcherConfig) -> None:
        """
        Args:
            config: handler configuration with parameters for Kiss-ICP scan matcher.
        """
        self._sensor_name = config.sensor_name
        cfg = self._to_kiss_icp_config(config)
        self._scan_matcher = KissICP(cfg)
        self._elements_queue: list[Element] = []
        self._noise_covariance = config.measurement_noise_covariance
        self._previous_pose: NumpyMatrix4x4 = np.eye(4)

        # self._visualizer = RegistrationVisualizer()
        # self._visualizer.global_view = True

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._sensor_name

    @property
    def sensor_type(self) -> type[Lidar3D]:
        """Lidar 3D sensor type."""
        return Lidar3D

    def process(self, element: Element) -> OdometryWithElements | None:
        """Computes the transformation SE(3) matrix between 2 point clouds. Always
        returns None for the very first element, as the transformation can not be
        computed for a single point cloud.

        Args:
            element: element with raw pointcloud data.

        Returns:
            measurement or None.

        Raises:
            TypeError: if the sensor is not an instance of Lidar3D.
        """
        if not isinstance(element.measurement.sensor, Lidar3D):
            msg = f"Expected sensor of type {Lidar3D}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        sensor = element.measurement.sensor

        tf_base_sensor = np.array(sensor.tf_base_sensor)
        tf_base_sensor_inv = np.linalg.inv(tf_base_sensor)

        self._elements_queue.append(element)

        point_cloud: np.ndarray = self._tuple_to_array(element.measurement.values)

        timestamp = element.timestamp

        _, _ = self._scan_matcher.register_frame(frame=point_cloud, timestamps=[timestamp])

        # self._visualizer.update(
        #     source, keypoints, self._scan_matcher.local_map, self._scan_matcher.poses[-1]
        # )

        if len(self._elements_queue) == self._elements_queue_size:

            current_pose = self._scan_matcher.last_pose

            tf_local = self._transformation(self._previous_pose, current_pose)
            tf_base = tf_base_sensor @ tf_local @ tf_base_sensor_inv

            new_measurement = self._create_measurement(tf_base)

            self._elements_queue.pop(0)

            self._previous_pose = current_pose

            return new_measurement

        return None

    @staticmethod
    def _to_kiss_icp_config(config: KissIcpScanMatcherConfig) -> KISSConfig:
        """Creates KissICP config with parameters from the handler config.

        Args:
            config: handler config.

        Returns:
            KissICP config.
        """
        kiss_cfg = KISSConfig()
        kiss_cfg.mapping.max_points_per_voxel = config.max_points_per_voxel
        kiss_cfg.mapping.voxel_size = config.voxel_size
        kiss_cfg.adaptive_threshold.initial_threshold = config.adaptive_initial_threshold
        kiss_cfg.data.min_range = config.min_range
        kiss_cfg.data.max_range = config.max_range
        kiss_cfg.data.deskew = config.deskew
        return kiss_cfg

    @staticmethod
    def _transformation(pose_i: NumpyMatrix4x4, pose_j: NumpyMatrix4x4) -> NumpyMatrix4x4:
        """Computes the transformation between two poses: T = inv(Pi) @ Pj.

        Args:
            pose_i: SE(3) matrix.

            pose_j: SE(3) matrix.

        Returns:
            transformation matrix SE(3).
        """
        tf = np.linalg.inv(pose_i) @ pose_j
        return tf

    def _tuple_to_array(self, values: tuple[float, ...]) -> np.ndarray:
        """Converts raw lidar data to numpy array of shape [N,3].

        Args:
            values: raw lidar scan data.

        Returns:
            raw values as a numpy array [N,3].
        """
        arr = np.array(values)
        arr = arr.reshape(-1, self._num_channels)
        return arr[:, :3]

    def _create_measurement(self, tf: NumpyMatrix4x4) -> OdometryWithElements:
        """Creates the measurement with the computed transformation matrix.

        Args:
            tf: transformation matrix SE(3).

        Returns:
            measurement with the transformation matrix.
        """
        pre_last_el = self._elements_queue[-2]
        last_el = self._elements_queue[-1]

        empty_pre_last_element = create_empty_element(pre_last_el)
        empty_last_element = create_empty_element(last_el)

        start = pre_last_el.timestamp
        stop = last_el.timestamp

        t_range = TimeRange(start, stop)

        cov = self._noise_covariance
        position_covariance = self._get_diagonal_matrix(cov[0], cov[1], cov[2])
        orientation_covariance = self._get_diagonal_matrix(cov[3], cov[4], cov[5])

        pose = self._numpy_matrix_4x4_to_matrix_4x4(tf)

        m = OdometryWithElements(
            stop,
            t_range,
            pose,
            position_covariance,
            orientation_covariance,
            elements=[empty_pre_last_element, empty_last_element],
        )
        return m

    @staticmethod
    def _get_diagonal_matrix(v1: float, v2: float, v3: float) -> Matrix3x3:
        return (
            (v1, 0.0, 0.0),
            (0.0, v2, 0.0),
            (0.0, 0.0, v3),
        )

    @staticmethod
    def _numpy_matrix_4x4_to_matrix_4x4(matrix: NumpyMatrix4x4) -> Matrix4x4:
        """Converts numpy matrix of size 4x4 to tuple of tuples of size 4x4.

        Args:
            matrix: numpy matrix of size 4x4.

        Returns:
            tuple of tuples of size 4x4.
        """
        if matrix.shape != (4, 4):
            raise ValueError("Input array must have shape (4, 4)")
        m = matrix
        return (
            (m[0, 0], m[0, 1], m[0, 2], m[0, 3]),
            (m[1, 0], m[1, 1], m[1, 2], m[1, 3]),
            (m[2, 0], m[2, 1], m[2, 2], m[2, 3]),
            (m[3, 0], m[3, 1], m[3, 2], m[3, 3]),
        )
