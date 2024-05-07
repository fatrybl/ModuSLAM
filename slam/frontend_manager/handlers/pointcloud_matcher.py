import logging

import numpy as np
from kiss_icp.kiss_icp import KISSConfig, KissICP

from slam.data_manager.factory.element import Element, RawMeasurement
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.frontend_manager.measurement_storage import Measurement
from slam.logger.logging_config import frontend_manager
from slam.setup_manager.sensors_factory.sensors import Lidar3D
from slam.system_configs.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from slam.utils.auxiliary_dataclasses import TimeRange

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
        super().__init__(config)
        cfg: KISSConfig = self._to_kiss_icp_config(config)
        self._scan_matcher = KissICP(cfg)
        self._elements_queue: list[Element] = []
        self._measurement_noise_covariance = config.measurement_noise_covariance

        # self._visualizer = RegistrationVisualizer()
        # self._visualizer.global_view = True

    def process(self, element: Element) -> Measurement | None:
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
        if isinstance(element.measurement.sensor, Lidar3D):
            sensor: Lidar3D = element.measurement.sensor
        else:
            msg = f"ScanMatcher can not process data from sensor {element.measurement.sensor!r}."
            logger.error(msg)
            raise TypeError(msg)

        new_measurement: Measurement | None = None

        tf_base_sensor = sensor.tf_base_sensor
        tf_base_sensor_inv = np.linalg.inv(tf_base_sensor)

        self._elements_queue.append(element)

        point_cloud: np.ndarray = self._tuple_to_array(element.measurement.values)

        timestamp = element.timestamp

        source, keypoints = self._scan_matcher.register_frame(
            frame=point_cloud, timestamps=[timestamp]
        )

        # self._visualizer.update(
        #     source, keypoints, self._scan_matcher.local_map, self._scan_matcher.poses[-1]
        # )

        if len(self._elements_queue) == self._elements_queue_size:
            prev_pose = self._scan_matcher.poses[-2]
            cur_pose = self._scan_matcher.poses[-1]

            tf_local = self._transformation(prev_pose, cur_pose)
            tf_base = tf_base_sensor @ tf_local @ tf_base_sensor_inv

            new_measurement = self._create_measurement(tf_base)

            self._update_queues()

        return new_measurement

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
        kiss_cfg.data.preprocess = config.preprocess
        return kiss_cfg

    @staticmethod
    def _transformation(pose_i: np.ndarray, pose_j: np.ndarray) -> np.ndarray:
        """Computes the transformation between two poses: T = inv(Pi) @ Pj.

        Args:
            pose_i (np.ndarray): SE(3) matrix.

            pose_j (np.ndarray): SE(3) matrix.

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

    def _create_measurement(self, tf: np.ndarray) -> Measurement:
        """Creates the measurement with the computed transformation matrix.

        Args:
            tf: transformation matrix SE(3).

        Returns:
            measurement with the transformation matrix.
        """
        last_el = self._elements_queue[-1]
        pre_last_el = self._elements_queue[-2]
        empty_m = RawMeasurement(sensor=last_el.measurement.sensor, values=())
        empty_pre_last_element = Element(
            timestamp=pre_last_el.timestamp, measurement=empty_m, location=pre_last_el.location
        )
        empty_last_element = Element(
            timestamp=last_el.timestamp, measurement=empty_m, location=last_el.location
        )
        start = pre_last_el.timestamp
        stop = last_el.timestamp

        t_range = TimeRange(start, stop)

        m = Measurement(
            handler=self,
            elements=(empty_pre_last_element, empty_last_element),
            time_range=t_range,
            values=tf,
            noise_covariance=self._measurement_noise_covariance,
        )
        return m

    def _update_queues(self):
        """Remove the oldest element and pose from the queue."""
        self._scan_matcher.poses.pop(0)
        self._elements_queue.pop(0)
