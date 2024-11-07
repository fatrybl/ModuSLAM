"""Preprocesses the GPS data for VRS_GPS sensor of Kaist Urban dataset."""

import logging

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.sensors_factory.sensors import VrsGps
from moduslam.utils.auxiliary_methods import create_empty_element, to_float, to_int
from phd.measurements.processed_measurements import Gps
from phd.moduslam.custom_types.aliases import Matrix3x3, Vector3
from phd.moduslam.frontend_manager.handlers.handler_protocol import Handler
from phd.moduslam.frontend_manager.handlers.vrs_gps.config import VrsGpsHandlerConfig

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

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._sensor_name

    @property
    def sensor_type(self) -> type[VrsGps]:
        """Type of VRS GPS sensor."""
        return VrsGps

    def process(self, element: Element) -> Gps | None:
        """Preprocesses the GPS data.

        Args:
            element: GPS data.

        Returns:
            measurement with GPS data or None.

        Raises:
            TypeError: If the sensor of the measurement is not VrsGps.
        """
        if not isinstance(element.measurement.sensor, VrsGps):
            msg = f"Expected sensor of type {VrsGps}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        fix_status = to_int(element.measurement.values[5])
        if fix_status not in self._fix_statuses:
            return None

        position = self._get_position(element.measurement.values)
        covariance = self._get_covariance(element.measurement.values)

        empty_element = self.create_empty_element(element)

        return Gps(empty_element, position, covariance)

    @staticmethod
    def create_empty_element(element: Element) -> Element:
        """
        Creates an empty element with the same timestamp, location and sensor as the input element.
        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without data.
        """
        return create_empty_element(element)

    @staticmethod
    def _get_position(data: list[str]) -> Vector3:
        """Gets position values from the element created from Kaist Urban dataset.

        Args:
            data: an element of Kaist Urban dataset.

        Returns:
            x, y, z coordinates.
        """
        d = data[2:5]
        position_xyz = (to_float(d[0]), to_float(d[1]), to_float(d[2]))
        return position_xyz

    @staticmethod
    def _get_covariance(data: list[str]) -> Matrix3x3:
        """Gets the covariance matrix from the element created from Kaist Urban dataset.

        Args:
            data: an element of Kaist Urban dataset.

        Returns:
            covariance matrix.
        """
        standard_deviation_str = data[8:11]
        sigma_x = to_float(standard_deviation_str[0])
        sigma_y = to_float(standard_deviation_str[1])
        sigma_z = to_float(standard_deviation_str[2])
        return (
            (sigma_x**2, 0.0, 0.0),
            (0.0, sigma_y**2, 0.0),
            (0.0, 0.0, sigma_z**2),
        )
