"""ImuOdometryFactory class.

Based on
https://github.com/borglab/gtsam/blob/develop/python/gtsam/examples/CombinedImuFactorExample.py
"""

import logging
from collections.abc import Collection

import gtsam

from slam.data_manager.factory.element import Element
from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.edge_factories.imu_preintegration.methods import (
    compute_covariance,
    create_edge,
    create_vertex,
    set_parameters,
)
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.custom_edges import ImuOdometry
from slam.frontend_manager.graph.custom_vertices import ImuBias, Pose, Velocity
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.frontend_manager.handlers.imu_data_preprocessor import ImuData
from slam.frontend_manager.measurement_storage import Measurement
from slam.logger.logging_config import frontend_manager
from slam.setup_manager.sensors_factory.sensors import Imu
from slam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.numpy_types import Vector3
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class ImuOdometryFactory(EdgeFactory):
    """
    Creates edges of type: ImuOdometry.
    """

    _gravity: float = 9.81
    _second: float = 1e9  # nanoseconds in 1 second.
    _nanosecond: float = 1e-9  # 1 nanosecond in seconds.

    def __init__(self, config: EdgeFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        super().__init__(config)
        self._time_margin: float = config.search_time_margin * self._second
        self._params = gtsam.PreintegrationCombinedParams.MakeSharedU(self._gravity)

    @property
    def vertices_types(self) -> set[type[Pose | Velocity | ImuBias]]:
        """Types of the used vertices."""
        return {Pose, Velocity, ImuBias}

    @property
    def base_vertices_types(
        self,
    ) -> set[type[gtsam.Pose3 | Vector3 | gtsam.imuBias.ConstantBias]]:
        """Types of the used base (GTSAM) instances."""
        return {gtsam.Pose3, Vector3, gtsam.imuBias.ConstantBias}

    def create(
        self,
        graph: Graph,
        vertices: Collection[Pose | Velocity | ImuBias],
        measurements: OrderedSet[Measurement],
    ) -> list[ImuOdometry]:
        """Creates new edges from the given measurements.

        Args:
            graph: the main graph.

            vertices: graph vertices to be used for new edges.

            measurements: measurements from different handlers.

        Returns:
            new edges.

        Raises:
            TypeError: if the vertex is not of type Pose, Velocity or ImuBias.
        """
        m = measurements.first

        for vertex in vertices:
            if isinstance(vertex, Pose):
                current_pose = vertex
            elif isinstance(vertex, Velocity):
                current_velocity = vertex
            elif isinstance(vertex, ImuBias):
                current_bias = vertex
            else:
                msg = f"Unknown vertex type: {type(vertex)}"
                logger.critical(msg)
                raise TypeError(msg)

        previous_pose = self._get_previous_vertex(
            graph.vertex_storage, m.time_range.start, current_pose.index, Pose
        )
        previous_velocity = self._get_previous_vertex(
            graph.vertex_storage, m.time_range.start, current_velocity.index, Velocity
        )
        previous_bias = self._get_previous_vertex(
            graph.vertex_storage, m.time_range.start, current_bias.index, ImuBias
        )

        previous_velocity.index = previous_pose.index
        previous_velocity.timestamp = previous_pose.timestamp
        previous_bias.index = previous_pose.index
        previous_bias.timestamp = previous_pose.timestamp

        pim = self._preintegrate_measurements(measurements, current_pose.timestamp)

        edge = create_edge(
            previous_pose,
            previous_velocity,
            previous_bias,
            current_pose,
            current_velocity,
            current_bias,
            measurements.items,
            pim,
        )

        return [edge]

    def _get_previous_vertex(
        self, storage: VertexStorage, timestamp: int, index: int, vertex_type: type[GraphVertex]
    ) -> GraphVertex:
        """Gets previous vertex if found or creates a new one.

        Args:
            storage: storage of vertices.

            timestamp: timestamp of the vertex.

            index: index of the vertex.

            vertex_type: type of the vertex.

        Returns:
            vertex.
        """

        vertex = storage.get_last_vertex(vertex_type)
        if vertex and vertex.timestamp == timestamp:
            return vertex

        vertex = storage.find_closest_optimizable_vertex(vertex_type, timestamp, self._time_margin)
        if vertex:
            return vertex
        else:
            new_index = index + 1
            new_vertex: GraphVertex = create_vertex(
                vertex_type=vertex_type, index=new_index, timestamp=timestamp
            )
            return new_vertex

    def _preintegrate_measurements(
        self,
        measurements: OrderedSet[Measurement],
        timestamp: int,
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

        if isinstance(element.measurement.sensor, Imu):

            accelerometer_noise_covariance, gyroscope_noise_covariance = compute_covariance(
                measurements
            )

            set_parameters(
                self._params,
                element.measurement.sensor.tf_base_sensor,
                accelerometer_noise_covariance,
                gyroscope_noise_covariance,
                element.measurement.sensor.integration_noise_covariance,
                element.measurement.sensor.accelerometer_bias_noise_covariance,
                element.measurement.sensor.gyroscope_bias_noise_covariance,
            )

        else:
            msg = f"Expected sensor of type {Imu}, got {type(element.measurement.sensor)}"
            logger.critical(msg)
            raise TypeError(msg)

        pim = gtsam.PreintegratedCombinedMeasurements(self._params)
        pim = self._integrate(pim, measurements, timestamp)
        return pim

    def _integrate(
        self,
        pim: gtsam.PreintegratedCombinedMeasurements,
        measurements: OrderedSet[Measurement],
        timestamp: int,
    ) -> gtsam.PreintegratedCombinedMeasurements:

        measurements_list = list(measurements)
        num_elements = len(measurements_list)

        for idx, m in enumerate(measurements):

            if idx == num_elements - 1:
                dt_nanoseconds = timestamp - measurements.last.time_range.start

            else:
                dt_nanoseconds = measurements_list[idx + 1].time_range.start - m.time_range.start

            values: ImuData = m.values
            acc = values.acceleration
            omega = values.angular_velocity

            dt_secs: float = dt_nanoseconds * self._nanosecond
            pim.integrateMeasurement(acc, omega, dt_secs)

        return pim
