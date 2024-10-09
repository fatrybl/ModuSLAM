from collections.abc import Sequence
from typing import Any

from phd.external.objects.measurements import ContinuousMeasurement, DiscreteMeasurement


class Odometry:
    def __init__(self, start: int, stop: int, value: Any):
        self.start = start
        self.stop = stop
        self.value = value


class Sorter:
    """Sorts measurements to groups: Discrete or Continuous."""

    _discrete_types = ()
    _continuous_types = ()

    @classmethod
    def sort_measurements(
        cls,
        measurements: Sequence,
    ) -> tuple[list[DiscreteMeasurement], list[ContinuousMeasurement]]:
        """Sorts measurements to Discrete and Continuous.

        Args:
            measurements: measurements to sort.

        Returns:
            discrete & continuous measurements.
        """
        discrete = []
        continuous = []

        for m in measurements:
            type_m = type(m)

            if isinstance(m, cls._discrete_types):
                discrete.append(m)
                continue

            if type_m in cls._continuous_types:
                continuous.append(m)
                continue

            else:
                raise TypeError(f"Is a type {type_m} discrete or continuous ?")

        return discrete, continuous


class MeasurementSplitter:
    @staticmethod
    def split(measurement: Odometry) -> tuple[DiscreteMeasurement, DiscreteMeasurement]:
        """Splits odometry-based measurement into 2 measurements with the same value but
        different timestamps.

        Args:
            measurement: measurement to split.

        Returns:
            2 discrete measurements with the same value.
        """
        m1 = DiscreteMeasurement(timestamp=measurement.start, value=measurement.value)
        m2 = DiscreteMeasurement(timestamp=measurement.stop, value=measurement.value)
        return m1, m2
