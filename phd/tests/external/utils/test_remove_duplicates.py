from phd.bridge.objects.auxiliary_classes import PseudoMeasurement
from phd.bridge.objects.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.objects.measurements_cluster import Cluster
from phd.external.utils import remove_duplicates
from phd.measurements.processed_measurements import ContinuousMeasurement


def test_remove_duplicates_empty_input():
    result = remove_duplicates([])
    assert result == []


def test_remove_duplicates_all_unique():
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()

    cluster1.add(PseudoMeasurement(1, "a"))
    cluster2.add(PseudoMeasurement(2, "b"))
    cluster3.add(PseudoMeasurement(3, "c"))

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster3], leftovers=[])

    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)
    assert result == input_list


def test_remove_duplicates_with_identical_measurements_and_leftovers():
    cluster1, cluster2 = Cluster(), Cluster()

    measurement1 = PseudoMeasurement(1, "a")
    measurement2 = PseudoMeasurement(2, "b")

    cluster1.add(measurement1)
    cluster2.add(measurement2)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[measurement2])

    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)
    expected_result = [clusters_with_leftovers_1, clusters_with_leftovers_3]

    assert result == expected_result


def test_remove_duplicates_with_continuous_measurements():
    cluster1, cluster2 = Cluster(), Cluster()

    m1 = PseudoMeasurement(1, 1)
    m2 = PseudoMeasurement(2, 1)
    m3 = PseudoMeasurement(3, 1)
    m4 = PseudoMeasurement(4, 1)

    continuous_measurement1 = ContinuousMeasurement(measurements=[m1, m2])
    continuous_measurement2 = ContinuousMeasurement(measurements=[m3, m4])

    cluster1.add(continuous_measurement1)
    cluster2.add(continuous_measurement2)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m3, m4])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m3, m4])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster1, cluster2], leftovers=[])

    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)
    expected_result = [clusters_with_leftovers_1, clusters_with_leftovers_3]

    assert result == expected_result


def test_remove_duplicates_all_duplicates():
    cluster1 = Cluster()
    measurement1 = PseudoMeasurement(1, "a")
    cluster1.add(measurement1)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])

    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)
    expected_result = [clusters_with_leftovers_1]

    assert result == expected_result


def test_remove_duplicates_identical_measurements_different_leftovers():
    cluster1, cluster2 = Cluster(), Cluster()

    measurement1 = PseudoMeasurement(1, "a")
    measurement2 = PseudoMeasurement(2, "b")

    cluster1.add(measurement1)
    cluster2.add(measurement2)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement2])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[measurement2])

    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)
    expected_result = [
        clusters_with_leftovers_1,
        clusters_with_leftovers_2,
        clusters_with_leftovers_3,
    ]

    assert result == expected_result


def test_remove_duplicates_identical_continuous_different_core_measurements():
    cluster1, cluster2 = Cluster(), Cluster()

    m1 = PseudoMeasurement(1, 1)
    m2 = PseudoMeasurement(2, 1)
    continuous_measurement = ContinuousMeasurement(measurements=[m1, m2])

    core_measurement1 = PseudoMeasurement(3, "a")
    core_measurement2 = PseudoMeasurement(4, "b")

    cluster1.add(continuous_measurement)
    cluster1.add(core_measurement1)

    cluster2.add(continuous_measurement)
    cluster2.add(core_measurement2)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[])

    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2]

    result = remove_duplicates(input_list)
    expected_result = [clusters_with_leftovers_1, clusters_with_leftovers_2]

    assert result == expected_result
