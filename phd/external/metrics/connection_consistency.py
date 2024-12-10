from phd.bridge.auxiliary_dataclasses import Connection
from phd.external.metrics.base_metric_protocol import Metrics
from phd.external.utils import get_subsequence
from phd.measurement_storage.cluster import Cluster
from phd.measurement_storage.measurements.auxiliary import PseudoMeasurement
from phd.measurement_storage.measurements.with_raw_elements import (
    ContinuousMeasurement,
    Measurement,
)


class EdgeConsistency(Metrics):

    @classmethod
    def compute(cls, connections: list[Connection], measurement: ContinuousMeasurement) -> bool:
        """Checks if edges are consistent: every edge has measurements in between.

        Args:
             connections: connections to be evaluated.

             measurement: continuous measurement to check.

        Returns:
            consistency status.
        """

        for connection in connections:
            t1 = connection.cluster1.timestamp
            t2 = connection.cluster2.timestamp
            num_elements = cls._num_elements_in_range(measurement.items, t1, t2)
            if num_elements == 0:
                return False

        return True

    @staticmethod
    def _num_elements_in_range(measurements: list[Measurement], start: int, stop: int) -> int:
        """Counts the number of elements in a sorted sequence that are within the range
        [start, stop].

        Args:
            measurements: discrete measurements sorted by timestamp.

            start: The lower bound of the range (inclusive).

            stop: The upper bound of the range (inclusive).

        Returns:
            The number of elements within the specified range.
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

    c1, c2, c3 = Cluster(), Cluster(), Cluster()

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
