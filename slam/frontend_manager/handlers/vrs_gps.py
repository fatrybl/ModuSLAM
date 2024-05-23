"""Preprocesses the GPS data for VRS_GPS sensor of Kaist Urban dataset."""

import logging

from slam.data_manager.factory.element import Element
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.frontend_manager.measurement_storage import Measurement
from slam.logger.logging_config import frontend_manager
from slam.setup_manager.sensors_factory.sensors import VrsGps
from slam.system_configs.frontend_manager.handlers.vrs_gps import VrsGpsHandlerConfig
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.auxiliary_methods import (
    create_empty_element,
    create_vector_3,
    to_float,
    to_int,
)
from slam.utils.numpy_types import Vector3

logger = logging.getLogger(frontend_manager)


class VrsGpsPreprocessor(Handler):

    def __init__(self, config: VrsGpsHandlerConfig) -> None:
        """
        Args:
            config: configuration of the handler.
        """
        super().__init__(config)
        self._fix_statuses: set[int] = set(config.fix_statuses)

    def process(self, element: Element) -> Measurement | None:
        """Preprocesses the GPS data.

        Args:
            element: GPS data.

        Returns:
            measurement with GPS data or None.
        """
        if not isinstance(element.measurement.sensor, VrsGps):
            msg = f"Expected sensor of type {VrsGps}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        fix_status = to_int(element.measurement.values[5])
        if fix_status not in self._fix_statuses:
            return None

        position_str: tuple[str, str, str] = element.measurement.values[2:5]
        standard_deviations_str = element.measurement.values[8:11]
        variances = tuple(to_float(x) ** 2 for x in standard_deviations_str)

        t = TimeRange(start=element.timestamp, stop=element.timestamp)

        empty_element = self._create_empty_element(element)

        position: Vector3 = create_vector_3(*position_str)

        m = Measurement(
            time_range=t,
            values=position,
            handler=self,
            elements=(empty_element,),
            noise_covariance=variances,
        )

        return m

    def _create_empty_element(self, element: Element) -> Element:
        """
        Creates an empty element with the same timestamp, location and sensor as the input element.
        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without data.
        """
        empty_element = create_empty_element(element)
        return empty_element
