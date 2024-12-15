"""Preprocesses the GPS data for VRS_GPS sensor of Kaist Urban dataset."""

import logging

from phd.external.handlers_factory.handlers.handler_protocol import Handler
from phd.external.handlers_factory.handlers.vrs_gps.config import VrsGpsHandlerConfig
from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.measurements.gps import Gps
from phd.moduslam.custom_types.aliases import Matrix3x3, Vector3
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.setup_manager.sensors_factory.sensors import VrsGps
from phd.moduslam.utils.auxiliary_methods import str_to_float, str_to_int

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
            TypeError: if the sensor of the measurement is not VrsGps.
        """
        if not isinstance(element.measurement.sensor, VrsGps):
            msg = f"Expected sensor of type {VrsGps}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        fix_status = str_to_int(element.measurement.values[5])
        if fix_status not in self._fix_statuses:
            return None

        position = self._get_position(element.measurement.values)
        covariance = self._get_covariance(element.measurement.values)

        return Gps(element.timestamp, position, covariance)

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
