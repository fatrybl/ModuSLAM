import logging

import numpy as np
from kiss_icp.kiss_icp import KISSConfig, KissICP

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.system_configs.system.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from slam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(__name__)


class ScanMatcher(Handler):

    _elements_queue_size: int = 2
    _num_channels: int = 4

    def __init__(self, config: KissIcpScanMatcherConfig) -> None:
        cfg: KISSConfig = self.to_kiss_icp_config(config)
        self._scan_matcher = KissICP(cfg)
        self._name: str = config.name
        self._elements_queue: list[Element] = []

        self._tf_extrinsic: np.ndarray = np.array(
            [
                [-0.514521, 0.701075, -0.493723, -0.333596],
                [-0.492472, -0.712956, -0.499164, -0.373928],
                [-0.701954, -0.0136853, 0.712091, 1.94377],
                [0, 0, 0, 1],
            ]
        )

        self._tf_extrinsic_inv = np.linalg.inv(self._tf_extrinsic)

        # self._visualizer = RegistrationVisualizer()
        # self._visualizer.global_view = True

    @property
    def name(self) -> str:
        return self._name

    @staticmethod
    def to_kiss_icp_config(cfg: KissIcpScanMatcherConfig) -> KISSConfig:
        """
        Creates KissICP config with parameters from the handler config.
        Args:
            cfg (KissIcpScanMatcherConfig): handler config.

        Returns:
            (KISSConfig): KissICP config.
        """
        kiss_cfg = KISSConfig()
        kiss_cfg.mapping.max_points_per_voxel = cfg.max_points_per_voxel
        kiss_cfg.mapping.voxel_size = cfg.voxel_size
        kiss_cfg.adaptive_threshold.initial_threshold = cfg.adaptive_initial_threshold
        kiss_cfg.data.min_range = cfg.min_range
        kiss_cfg.data.max_range = cfg.max_range
        kiss_cfg.data.deskew = cfg.deskew
        kiss_cfg.data.preprocess = cfg.preprocess
        return kiss_cfg

    def tuple_to_array(self, values: tuple[float, ...]) -> np.ndarray:
        """
        Converts raw lidar data to numpy array of shape [Nx3].
        Args:
            values (tuple[float,...]): raw lidar scan data.

        Returns:
            (np.ndarray[Nx3]): raw values as a numpy array.

        """
        arr = np.array(values)
        arr = arr.reshape(-1, self._num_channels)
        return arr[:, :3]

    @staticmethod
    def _transformation(pose_i: np.ndarray, pose_j: np.ndarray) -> np.ndarray:
        """
        Compute the transformation between two poses as SE(3) matrices:
            T = inv(Pi) @ Pj
        Args:
            pose_i (np.ndarray): SE(3) matrix.
            pose_j (np.ndarray): SE(3) matrix.

        Returns:
            (np.ndarray): transformation matrix SE(3).
        """
        tf = np.linalg.inv(pose_i) @ pose_j
        return tf

    def _create_measurement(self, tf: np.ndarray) -> Measurement:
        """
        Creates a Measurement object with the computed transformation matrix.
        Args:
            tf (np.ndarray[4x4]): transformation matrix SE(3).

        Returns:
            (Measurement): measurement with the computed transformation matrix SE(3).
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
        )
        return m

    def _update_queues(self):
        """Remove the oldest element and pose."""
        self._scan_matcher.poses.pop(0)
        self._elements_queue.pop(0)

    def process(self, element: Element) -> Measurement | None:
        """Computes the transformation as SE(3) matrix between 2 point clouds. Always
        returns None for the very first element, as the transformation can not be
        computed for a single point cloud.

        Args:
            element (Element): element with raw pointcloud data.

        Returns:
            measurement (Measurement): measurement with the computed transformation matrix SE(3).
            (None): if the transformation can not be computed.
        """
        new_measurement: Measurement | None = None

        self._elements_queue.append(element)

        point_cloud: np.ndarray = self.tuple_to_array(element.measurement.values)

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
            tf_base = self._tf_extrinsic @ tf_local @ self._tf_extrinsic_inv

            new_measurement = self._create_measurement(tf_base)

            self._update_queues()

        return new_measurement
