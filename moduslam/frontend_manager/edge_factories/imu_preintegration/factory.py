"""ImuOdometryFactory class.

Based on
https://github.com/borglab/gtsam/blob/develop/python/gtsam/examples/CombinedImuFactorExample.py
"""

import logging

import gtsam

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from moduslam.frontend_manager.edge_factories.imu_preintegration.utils import (
    compute_covariance,
    create_edge,
    get_vertices,
    integrate,
    set_parameters,
)
from moduslam.frontend_manager.graph.custom_edges import ImuOdometry
from moduslam.frontend_manager.graph.custom_vertices import (
    ImuBias,
    LinearVelocity,
    Pose,
)
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.sensors_factory.sensors import Imu
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class ImuOdometryFactory(EdgeFactory):
    """
    Creates edges of type: ImuOdometry.
    """

    _gravity: float = 9.81
    _second: float = 1e9  # nanoseconds in 1 second.
    _nanosecond: float = 1e-9  # 1 nanosecond in seconds.
    _minimum_number_of_measurements: int = 4

    def __init__(self, config: EdgeFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        super().__init__(config)
        self._time_margin = int(config.search_time_margin * self._second)
        self._params = gtsam.PreintegrationCombinedParams.MakeSharedU(self._gravity)

    def create(
        self,
        graph: Graph,
        measurements: OrderedSet[Measurement],
        timestamp: int,
    ) -> list[ImuOdometry]:
        """Creates new edges from the given measurements.

        Args:
            graph: the main graph.

            measurements: measurements from different handlers.

            timestamp: timestamp to integrate the measurements up to.

        Returns:
            new edges.

        Raises:
            TypeError: if the vertex is not of type Pose, Velocity or ImuBias.
        """
        if len(measurements) < self._minimum_number_of_measurements:
            logger.error(
                f"Number of measurements is less than {self._minimum_number_of_measurements}."
            )
            return []

        t_start = measurements.first.time_range.start
        t_stop = timestamp

        previous_vertices = get_vertices(graph.vertex_storage, t_start, self._time_margin)
        pose_i, velocity_i, bias_i, new_index_flag_i = previous_vertices

        if new_index_flag_i:
            current_vertices = get_vertices(
                graph.vertex_storage,
                t_stop,
                self._time_margin,
                index=pose_i.index + 1,
            )
        else:
            current_vertices = get_vertices(
                graph.vertex_storage,
                t_stop,
                self._time_margin,
                default_values=(pose_i.value, velocity_i.value, bias_i.value),
            )
        pose_j, velocity_j, bias_j, new_index_flag_j = current_vertices

        if new_index_flag_i and not new_index_flag_j:
            index = pose_i.index
            t = pose_i.timestamp
            pose_i = Pose(timestamp=t, index=index, value=pose_j.value)
            velocity_i = LinearVelocity(timestamp=t, index=index, value=velocity_j.value)
            bias_i = ImuBias(timestamp=t, index=index, value=bias_j.value)

        if pose_i.gtsam_index == pose_j.gtsam_index:
            logger.error("Pose-i and Pose-j are the same!")
            return []

        if velocity_i.gtsam_index == velocity_j.gtsam_index:
            logger.error("Velocity-i and Velocity-j are the same!")
            return []

        if bias_i.gtsam_index == bias_j.gtsam_index:
            logger.error("Bias-i and Bias-j are the same!")
            return []

        biases = bias_i.gtsam_instance

        pim = self._preintegrate_measurements(measurements, pose_j.timestamp, biases)

        edge = create_edge(
            pose_i,
            velocity_i,
            bias_i,
            pose_j,
            velocity_j,
            bias_j,
            measurements.items,
            pim,
        )

        return [edge]

    def _preintegrate_measurements(
        self,
        measurements: OrderedSet[Measurement],
        timestamp: int,
        bias: gtsam.imuBias.ConstantBias,
    ) -> gtsam.PreintegratedCombinedMeasurements:
        """Integrates the IMU measurements.

        Last measurement timestamp and vertex timestamp are used to compute dt for integration of the last measurement.

        Args:
            measurements: IMU measurements.

            timestamp: timestamp of the vertex.

        Returns:
             preintegrated IMU measurements.
        """

        element: Element = measurements.first.elements[0]
        sensor = element.measurement.sensor

        if isinstance(sensor, Imu):

            if len(measurements) == self._minimum_number_of_measurements:

                accelerometer_noise_covariance = sensor.accelerometer_noise_covariance
                gyroscope_noise_covariance = sensor.gyroscope_noise_covariance

            else:

                accelerometer_noise_covariance, gyroscope_noise_covariance = compute_covariance(
                    measurements
                )

            set_parameters(
                self._params,
                sensor.tf_base_sensor,
                accelerometer_noise_covariance,
                gyroscope_noise_covariance,
                sensor.integration_noise_covariance,
                sensor.accelerometer_bias_noise_covariance,
                sensor.gyroscope_bias_noise_covariance,
            )

        else:
            msg = f"Expected sensor of type {Imu}, got {type(element.measurement.sensor)}"
            logger.critical(msg)
            raise TypeError(msg)

        pim = gtsam.PreintegratedCombinedMeasurements(self._params)
        pim.resetIntegrationAndSetBias(bias)
        pim = integrate(pim, measurements, timestamp, self._nanosecond)

        return pim
