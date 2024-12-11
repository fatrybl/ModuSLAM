"""TODO: add tests."""

from phd.bridge.auxiliary_dataclasses import Connection
from phd.external.metrics.base import Metrics
from phd.external.utils import get_subsequence
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.auxiliary import PseudoMeasurement
from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.continuous import ContinuousMeasurement


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
        """Counts the number of elements in a sorted sequence that are within the range
        [start, stop].

        Args:
            measurements: discrete measurements sorted by timestamp.

            start: a lower bound of the range (inclusive).

            stop: an upper bound of the range (inclusive).

        Returns:
            a number of elements.
        """
        _, start_idx, stop_idx = get_subsequence(measurements, start, stop)
        return stop_idx - start_idx


if __name__ == "__main__":

    """Correct consistency example."""

    d1 = PseudoMeasurement(1, "a")
    d2 = PseudoMeasurement(4, "b")
    d3 = PseudoMeasurement(7, "c")

    m1 = PseudoMeasurement(1, 1)
    m2 = PseudoMeasurement(2, 1)
    m3 = PseudoMeasurement(5, 1)
    measurement = ContinuousMeasurement(measurements=[m1, m2, m3])

    c1, c2, c3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()

    c1.add(d1)
    c2.add(d2)
    c3.add(d3)

    con1, con2 = Connection(c1, c2), Connection(c2, c3)
    connections = [con1, con2]

    consistency = EdgeConsistency.compute(connections, measurement)
    print(f"Consistency status: {consistency}")
    """Incorrect consistency example."""

    m1 = PseudoMeasurement(4, 1)
    m2 = PseudoMeasurement(5, 1)
    m3 = PseudoMeasurement(6, 1)
    measurement = ContinuousMeasurement(measurements=[m1, m2, m3])

    connections = [Connection(c1, c2)]

    consistency = EdgeConsistency.compute(connections, measurement)
    print(f"Consistency status: {consistency}")
