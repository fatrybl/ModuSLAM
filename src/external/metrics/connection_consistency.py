"""Edge consistency check."""

from src.bridge.auxiliary_dataclasses import Connection
from src.external.metrics.base import Metrics
from src.external.utils import get_subsequence
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.continuous import ContinuousMeasurement


class EdgeConsistency(Metrics):

    @classmethod
    def compute(cls, connections: list[Connection], measurement: ContinuousMeasurement) -> bool:
        """Checks if edges are consistent: every edge has measurements in between.

        Args:
             connections: connections to be checked.

             measurement: a continuous measurement to check.

        Returns:
            consistency status.
        """

        for connection in connections:
            t1 = connection.cluster1.timestamp
            t2 = connection.cluster2.timestamp
            num_elements = cls._get_num_elements_between(measurement.items, t1, t2)
            if num_elements == 0:
                return False

        return True

    @staticmethod
    def _get_num_elements_between(measurements: list[Measurement], start: int, stop: int) -> int:
        """Get number of elements in a sorted sequence which are in the range [start,
        stop].

        Args:
            measurements: discrete measurements sorted by timestamp.

            start: a lower bound of the range (inclusive).

            stop: an upper bound of the range (inclusive).

        Returns:
            a number of elements.
        """
        _, start_idx, stop_idx = get_subsequence(measurements, start, stop)
        return stop_idx - start_idx
