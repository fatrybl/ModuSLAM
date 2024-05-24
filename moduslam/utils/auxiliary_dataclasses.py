"""This module contains auxiliary dataclasses that are used in the moduslam package.

Any dataclass that is used in multiple packages may be defined here.
"""

from dataclasses import dataclass

from moduslam.setup_manager.sensors_factory.sensors import Sensor


@dataclass(frozen=True, eq=True)
class TimeRange:
    """Represents time range with start/stop timestamps."""

    start: int
    stop: int

    def __post_init__(self) -> None:
        """Check if the start and stop timestamps are valid.

        Raises:
            ValueError: If start or stop timestamp is negative or if start is greater than stop.
        """
        if self.start < 0:
            raise ValueError(f"timestamp start={self.start} can not be negative")
        if self.stop < 0:
            raise ValueError(f"timestamp stop={self.stop} can not be negative")
        if self.start > self.stop:
            raise ValueError(
                f"timestamp start={self.start} can not be greater than stop={self.stop}"
            )


@dataclass(frozen=True, eq=True)
class PeriodicDataRequest:
    """A request for periodic data from a sensor with start/stop time margins."""

    sensor: Sensor
    period: TimeRange
