"""Base abstract measurements."""

from abc import ABC, abstractmethod

from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.utils.auxiliary_dataclasses import TimeRange


class Measurement(ABC):
    """Base absract measurement."""

    @property
    @abstractmethod
    def timestamp(self) -> int:
        """Timestamp of the measurement."""


class TimeRangeMeasurement(Measurement):
    """Protocol for measurement with the time range property."""

    @property
    @abstractmethod
    def time_range(self) -> TimeRange:
        """Measurement`s time range."""


class WithRawElements(Measurement):
    """Base measurement containing raw elements."""

    @property
    @abstractmethod
    def elements(self) -> list[Element]:
        """Raw elements used to form the measurement."""
