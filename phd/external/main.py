"""Main algorithm."""

from phd.external.combinations_factory import Factory
from phd.external.connections.utils import get_clusters_and_leftovers
from phd.external.objects.measurements import (
    ContinuousMeasurement,
    CoreMeasurement,
    Measurement,
    Odometry,
)
from phd.external.preprocessors.fake_measurement_factory import add_fake_if_needed
from phd.external.preprocessors.odometry_splitter import find_and_split, remove_odometry
from phd.external.preprocessors.utils import find_continuous_measurement
from phd.external.utils import group_by_timestamp, remove_duplicates

if __name__ == "__main__":

    d1 = CoreMeasurement(1, "a")
    d2 = CoreMeasurement(3, "b")
    d3 = CoreMeasurement(5, "c")
    # d4 = CoreMeasurement(7, "d")
    imu1 = CoreMeasurement(0, 0.5)
    imu2 = CoreMeasurement(1, 0.5)
    imu3 = CoreMeasurement(2, 0.5)
    # imu4 = CoreMeasurement(4, 0.5)
    # imu5 = CoreMeasurement(5, 0.5)
    # imu6 = DiscreteMeasurement(6, 0.5)
    imu = ContinuousMeasurement(elements=[imu1, imu2, imu3])
    odom1 = Odometry(1, 2, "o1")
    odom2 = Odometry(2, 3, "o2")

    measurements: list[Measurement] = [d1, d2, odom1]

    # ===============================================================================================

    odometry_measurements = find_and_split(measurements)
    if odometry_measurements:
        measurements = remove_odometry(measurements)
        measurements += odometry_measurements

    continuous_measurement = find_continuous_measurement(measurements)

    if continuous_measurement:
        measurements.remove(continuous_measurement)
        add_fake_if_needed(continuous_measurement, measurements)

    measurements.sort(key=lambda m: m.timestamp)

    groups = group_by_timestamp(measurements)

    clusters_combinations = Factory.combine(groups.values())
    clusters_combinations = Factory.remove_loops(clusters_combinations)

    if continuous_measurement:
        clusters_with_leftovers = get_clusters_and_leftovers(
            clusters_combinations, continuous_measurement
        )

        clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)

        for item in clusters_with_leftovers:
            print(item)

    else:
        for comb in clusters_combinations:
            print(comb)
