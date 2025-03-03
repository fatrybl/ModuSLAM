"""Preprocesses the GPS data for VRS_GPS sensor of Kaist Urban dataset."""

import logging

from src.custom_types.aliases import Matrix3x3, Matrix4x4, Vector3
from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.external.handlers_factory.handlers.vrs_gps.config import VrsGpsHandlerConfig
from src.logger.logging_config import frontend_manager
from src.measurement_storage.measurements.position import Position
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.sensors_factory.sensors import VrsGps
from src.utils.auxiliary_methods import str_to_float, str_to_int

logger = logging.getLogger(frontend_manager)


class KaistUrbanVrsGpsPreprocessor(Handler):
    """Processes measurements from the Kaist Urban dataset."""

    def __init__(self, config: VrsGpsHandlerConfig) -> None:
        """
        Args:
            config: configuration of the handler.
        """
        self._sensor_name: str = config.sensor_name
        self._fix_statuses: set[int] = set(config.fix_statuses)
        self._first_position: Vector3 | None = config.first_position

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._sensor_name

    @property
    def sensor_type(self) -> type[VrsGps]:
        """Type of VRS GPS sensor."""
        return VrsGps

    def process(self, element: Element) -> Position | None:
        """Preprocesses the GPS data.

        Args:
            element: GPS data.

        Returns:
            measurement with GPS data or None.

        Raises:
            TypeError: if the sensor of the measurement is not VrsGps.
        """
        sensor = element.measurement.sensor
        values = element.measurement.values

        if not isinstance(sensor, VrsGps):
            msg = f"Expected sensor of type {VrsGps}, got {type(sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        fix_status = str_to_int(values[5])
        if fix_status not in self._fix_statuses:
            return None

        position = self._get_position(values)

        if self._first_position:
            position = self._subtract_position(position, self._first_position)
        else:
            position = self._apply_transform(position, sensor.tf_base_sensor)

        covariance = self._get_covariance(values)

        return Position(element.timestamp, position, covariance)

    @staticmethod
    def _subtract_position(source: Vector3, target: Vector3) -> Vector3:
        """Subtracts two position vectors.

        Args:
            source: a source position.

            target: a target position.

        Returns:
            a position.
        """
        return (
            source[0] - target[0],
            source[1] - target[1],
            source[2] - target[2],
        )

    @staticmethod
    def _apply_transform(position: Vector3, tf: Matrix4x4) -> Vector3:
        """Applies base->sensor transformation to the measurement.

        Args:
            position: a position measurement.

            tf: a base->sensor SE(3) transformation.

        Returns:
            a transformed measurement.
        """
        position_base_sensor = (tf[0][3], tf[1][3], tf[2][3])
        return (
            position[0] - position_base_sensor[0],
            position[1] - position_base_sensor[1],
            position[2] - position_base_sensor[2],
        )

    @staticmethod
    def _get_position(data: list[str]) -> Vector3:
        """Gets position values from the element created from Kaist Urban dataset.

        Args:
            data: an element of Kaist Urban dataset.

        Returns:
            x, y, z coordinates.
        """
        d = data[2:5]
        position_xyz = (str_to_float(d[0]), str_to_float(d[1]), str_to_float(d[2]))
        return position_xyz

    @staticmethod
    def _get_covariance(data: list[str]) -> Matrix3x3:
        """Gets the covariance matrix from the element created from Kaist Urban dataset.

        Args:
            data: an element of Kaist Urban dataset.

        Returns:
            covariance matrix.
        """
        std = data[8:11]
        sigma_x = str_to_float(std[0])
        sigma_y = str_to_float(std[1])
        sigma_z = str_to_float(std[2])
        return (
            (sigma_x**2, 0.0, 0.0),
            (0.0, sigma_y**2, 0.0),
            (0.0, 0.0, sigma_z**2),
        )
