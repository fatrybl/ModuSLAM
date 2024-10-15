"""Main algorithm."""

from phd.external.merger import CombinationsFactory
from phd.external.objects.cluster import MeasurementsCluster
from phd.external.objects.measurements import (
    ContinuousMeasurement,
    CoreMeasurement,
    FakeMeasurement,
)
from phd.external.utils import get_clusters_and_leftovers, remove_duplicates

if __name__ == "__main__":

    d1 = CoreMeasurement(1, "a")
    d2 = CoreMeasurement(3, "b")
    d3 = CoreMeasurement(5, "c")
    # d4 = DiscreteMeasurement(7, "d")
    imu1 = CoreMeasurement(0, 0.5)
    imu2 = CoreMeasurement(1, 0.5)
    imu3 = CoreMeasurement(2, 0.5)
    imu4 = CoreMeasurement(4, 0.5)
    # imu5 = CoreMeasurement(5, 0.5)
    # imu6 = DiscreteMeasurement(6, 0.5)
    imu = ContinuousMeasurement(elements=[imu1, imu2, imu3])
    odom1 = Odometry(1, 2, "o1")
    odom2 = Odometry(2, 3, "o2")

    measurements: list[Measurement] = [d1, d2, odom1, imu, odom2]

    # ===============================================================================================

    odometry_measurements = find_and_split(measurements)
    if odometry_measurements:
        measurements = remove_odometry(measurements)
        measurements += odometry_measurements

    continuous_measurement = find_continuous_measurement(measurements)

    fake = FakeMeasurement(imu1.timestamp)

    discrete_measurements: list[CoreMeasurement | FakeMeasurement] = [fake, d1, d2, d3]
    # TODO: split odometry measurements to the pair of discrete measurements here.
    continuous_measurement = ContinuousMeasurement(elements=[imu1, imu2, imu3, imu4])

    clusters_combinations: list[list[MeasurementsCluster]] = CombinationsFactory.combine(
        discrete_measurements
    )

    groups = group_by_timestamp(measurements)

    clusters_combinations = Factory.combine(groups.values())
    clusters_combinations = remove_loops(clusters_combinations)

    if continuous_measurement:
        clusters_with_leftovers = get_clusters_and_leftovers(
            clusters_combinations, continuous_measurement
        )

        clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)

        for item in clusters_with_leftovers:
            print(item)

    unique_clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)

    print("=========================================================")

    for item in unique_clusters_with_leftovers:
        print(item)
