from collections.abc import Iterable

from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import FakeMeasurement
from moduslam.measurement_storage.measurements.base import Measurement


def add_fake_cluster(clusters: list[MeasurementCluster], timestamp: int) -> None:
    """Adds a cluster with a fake measurement to the beginning of the list based on the
    condition.

    Args:
        clusters: a list of clusters to add a new cluster to.

        timestamp: timestamp of the fake measurement.
    """
    cluster = MeasurementCluster()
    cluster.add(FakeMeasurement(timestamp))
    clusters.insert(0, cluster)


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
