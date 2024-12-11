from collections.abc import Iterable

from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.auxiliary import FakeMeasurement
from phd.measurement_storage.measurements.base import Measurement


def add_fake_cluster(list_to_add: list[MeasurementCluster], timestamp: int) -> None:
    """Adds a cluster with a fake measurement to the beginning of the list based on the
    condition.

    Args:
        list_to_add: a list of clusters to add a new cluster to.

        timestamp: timestamp of the fake measurement.
    """
    first_cluster = list_to_add[0]
    cluster_timestamp = first_cluster.timestamp

    if timestamp < cluster_timestamp:
        cluster = MeasurementCluster()
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
