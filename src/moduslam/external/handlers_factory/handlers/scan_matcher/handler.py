import logging

import numpy as np
from kiss_icp.kiss_icp import KISSConfig, KissICP

from moduslam.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from moduslam.custom_types.numpy import MatrixNx3
from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.utils import create_empty_element
from moduslam.external.handlers_factory.handlers.handler_protocol import Handler
from moduslam.external.handlers_factory.handlers.scan_matcher.config import (
    KissIcpScanMatcherConfig,
)
from moduslam.logger.logging_config import frontend_manager
from moduslam.measurement_storage.measurements.pose_odometry import OdometryWithElements
from moduslam.sensors_factory.sensors import Lidar3D
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_methods import (
    diagonal_matrix3x3,
    numpy_array4x4_to_tuple4x4,
)

logger = logging.getLogger(frontend_manager)


class ScanMatcher(Handler):
    """
    Handler computes the transformation between two point clouds based on Kiss-ICP method:
    https://github.com/PRBonn/kiss-icp.
    """

    _elements_queue_size: int = 2  # number of elements to compute the transformation

    def __init__(self, config: KissIcpScanMatcherConfig) -> None:
        """
        Args:
            config: handler configuration with parameters for Kiss-ICP scan matcher.
        """
        cfg = self._to_kiss_icp_config(config)
        self._sensor_name = config.sensor_name
        self._noise_covariance = config.measurement_noise_covariance
        self._scan_matcher = KissICP(cfg)
        self._elements_queue: list[Element] = []
        self._num_channels = config.num_channels

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
            element: element with raw point cloud data.

        Returns:
            measurement or None.

        Raises:
            TypeError: if the sensor is not an instance of Lidar3D.
        """
        sensor = element.measurement.sensor

        if not isinstance(sensor, Lidar3D):
            msg = f"Expected sensor of type {Lidar3D}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        tf_base_sensor = np.array(sensor.tf_base_sensor)
        tf_base_sensor_inv = np.linalg.inv(tf_base_sensor)
        timestamps = np.array([element.timestamp])

        self._elements_queue.append(element)

        point_cloud = self._tuple_to_array(element.measurement.values)

        self._scan_matcher.register_frame(point_cloud, timestamps)

        if len(self._elements_queue) == self._elements_queue_size:
            d_tf = self._scan_matcher.last_delta

            d_tf_base = tf_base_sensor @ d_tf @ tf_base_sensor_inv

            new_measurement = self._create_measurement(d_tf_base)

            self._elements_queue.pop(0)

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

    def _tuple_to_array(self, values: tuple[float, ...]) -> MatrixNx3:
        """Converts raw lidar data to numpy array of shape [N,3].

        Args:
            values: raw lidar scan data.

        Returns:
            raw values as a numpy array.
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
        position_covariance = diagonal_matrix3x3(cov[0:3])
        orientation_covariance = diagonal_matrix3x3(cov[3:])

        pose = numpy_array4x4_to_tuple4x4(tf)

        m = OdometryWithElements(
            stop,
            t_range,
            pose,
            position_covariance,
            orientation_covariance,
            elements=[empty_pre_last_element, empty_last_element],
        )
        return m
