import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Type

import numpy as np
import numpy.typing as npt

from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.elements_distributor.measurement import Measurement
from slam.frontend_manager.handlers.ABC_handler import ElementHandler
from slam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(__name__)


@dataclass
class Measurement:
    """
    A measurement obtained from the preprocessed element(s)
    """

    time_range: TimeRange
    values: Any
    type: Type[ElementHandler]
    elements: tuple[Element, ...]
    covariance: npt.NDArray[np.float64] | None = None


class MeasurementStorage:
    def __init__(self) -> None:
        self.data: dict[Type[ElementHandler], deque[Measurement]] = defaultdict(deque)
        self._last_timestamp: int | None = None

    @property
    def last_timestamp(self) -> int:
        """
        The timestamp of the last added measurement.
        Returns:
            (int): timestamp of the last added measurement.
        Raises:
            ValueError: if the timestamp is None.
        """
        if self.last_timestamp:
            return self._last_timestamp
        else:
            msg = "The last measurement timestamp is None."
            logger.error(msg)
            raise ValueError

    def delete(self, handler: Type[ElementHandler], z: Measurement) -> None:
        """
        Deletes the measurement from the storage.
        Args:
            handler (Type[ElementHandler]): element handler.
            z (Measurement): The measurement to be deleted.

        TODO: update last_timestamp when deleting the measurement.
        """
        self.data[handler].remove(z)

    def add(self, handler: Type[ElementHandler], z: Measurement) -> None:
        """
        Adds a new measurement to the storage and updates last_timestamp attribute.
        Args:
            handler (ElementHandler): element handler.
            z (Measurement): a new measurement to be added.
        """
        self.data[handler].append(z)
        self._last_timestamp = z.time_range.stop
