from collections.abc import Iterable

from phd.bridge.objects.auxiliary_classes import FakeMeasurement
from phd.bridge.objects.measurements_cluster import Cluster
from phd.measurements.processed_measurements import Measurement


def add_fake_cluster(list_to_add: list[Cluster], timestamp: int) -> None:
    """Adds a cluster with a fake measurement to the beginning of the list based on the
    condition.

    Args:
        list_to_add: a list of clusters to add a new cluster in.

        timestamp: timestamp of the fake measurement.

    TODO: check if correct start timestamp in used for the cluster:
        maybe we should use time_range.start instead of timestamp?
    """
    t1 = list_to_add[0].timestamp
    if timestamp < t1:
        cluster = Cluster()
        fake_measurement = FakeMeasurement(timestamp)
        cluster.add(fake_measurement)
        list_to_add.insert(0, cluster)


def find_fake_measurement(measurements: Iterable[Measurement]) -> FakeMeasurement | None:
    """Finds the 1-st fake measurement in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        the 1-st fake measurement if found or None.
    """
    for m in measurements:
        if isinstance(m, FakeMeasurement):
            return m
    return None
