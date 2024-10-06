"""Algorithm runner."""

from phd_thesis.src.merger import CombinationsFactory
from phd_thesis.src.objects.cluster import Cluster
from phd_thesis.src.objects.measurements import (
    ContinuousMeasurement,
    DiscreteMeasurement,
)
from phd_thesis.src.utils import create_clusters_with_leftovers_combinations

if __name__ == "__main__":

    d1 = DiscreteMeasurement(1, "a")
    d2 = DiscreteMeasurement(3, "b")
    d3 = DiscreteMeasurement(5, "c")
    # d4 = DiscreteMeasurement(7, "d")
    imu1 = DiscreteMeasurement(0, 0.5)
    imu2 = DiscreteMeasurement(1, 0.5)
    imu3 = DiscreteMeasurement(2, 0.5)
    imu4 = DiscreteMeasurement(4, 0.5)
    imu5 = DiscreteMeasurement(5, 0.5)
    # imu6 = DiscreteMeasurement(6, 0.5)

    discrete_measurements = [d1, d2, d3]
    # TODO: split odometry measurements to the pair of discrete measurements here.

    continuous_measurement = ContinuousMeasurement(elements=[imu1, imu2, imu3, imu4, imu5])

    clusters_combinations: list[list[Cluster]] = CombinationsFactory.combine(discrete_measurements)

    clusters_with_leftovers_combinations = create_clusters_with_leftovers_combinations(
        clusters_combinations, continuous_measurement
    )

    for comb in clusters_with_leftovers_combinations:
        print(comb)
