"""Main algorithm."""

from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.bridge.objects.auxiliary_classes import PseudoMeasurement
from phd.bridge.preprocessors.fake_measurement_factory import add_fake_if_needed
from phd.bridge.preprocessors.odometry_splitter import find_and_split, remove_odometry
from phd.external.combinations_factory import Factory
from phd.external.connections.utils import get_clusters_and_leftovers
from phd.external.utils import group_by_timestamp, remove_duplicates, remove_loops
from phd.measurements.processed_measurements import Measurement, PoseOdometry

if __name__ == "__main__":

    identity3 = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    identity4 = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )

    d1 = PseudoMeasurement(1, "a")
    d2 = PseudoMeasurement(3, "b")
    # d3 = CoreMeasurement(5, "c")
    # d4 = CoreMeasurement(7, "d")
    imu1 = PseudoMeasurement(0, 0.5)
    imu2 = PseudoMeasurement(1, 0.5)
    imu3 = PseudoMeasurement(2, 0.5)
    # imu4 = CoreMeasurement(4, 0.5)
    # imu5 = CoreMeasurement(5, 0.5)
    # imu6 = DiscreteMeasurement(6, 0.5)
    imu_readings: list[Measurement] = [imu1, imu2, imu3]
    odom1 = PoseOdometry(1, TimeRange(0, 1), identity4, identity3, identity3, [])
    odom2 = PoseOdometry(2, TimeRange(1, 2), identity4, identity3, identity3, [])

    measurements: list[Measurement] = [d1, d2, odom1, odom2]

    # ===============================================================================================

    split_odometry_measurements = find_and_split(measurements)
    if split_odometry_measurements:
        measurements = remove_odometry(measurements)
        measurements += split_odometry_measurements

    measurements.sort(key=lambda m: m.timestamp)

    if imu_readings:
        add_fake_if_needed(measurements, imu_readings)

    groups = group_by_timestamp(measurements)

    clusters_combinations = Factory.combine(groups.values())
    clusters_combinations = remove_loops(clusters_combinations)

    if imu_readings:
        clusters_with_leftovers = get_clusters_and_leftovers(clusters_combinations, imu_readings)

        clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)

        for item in clusters_with_leftovers:
            print(item)

    else:
        for comb in clusters_combinations:
            print(comb)
