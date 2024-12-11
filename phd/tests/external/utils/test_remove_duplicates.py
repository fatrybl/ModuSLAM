from phd.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from phd.external.utils import remove_duplicates
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.auxiliary import PseudoMeasurement
from phd.measurement_storage.measurements.continuous import ContinuousMeasurement


def test_remove_duplicates_empty_input():
    result = remove_duplicates([])
    assert result == []


def test_remove_duplicates_all_unique():
    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()

    cluster1.add(PseudoMeasurement(1, "a"))
    cluster2.add(PseudoMeasurement(2, "b"))
    cluster3.add(PseudoMeasurement(3, "c"))

    item1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[])
    item2 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[])
    item3 = ClustersWithLeftovers(clusters=[cluster3], leftovers=[])

    input_list = [item1, item2, item3]

    result = remove_duplicates(input_list)
    assert result == input_list


def test_remove_duplicates_with_identical_measurements_and_leftovers():
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()

    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")

    cluster1.add(m1)
    cluster2.add(m2)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m1])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m1])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[m2])
    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)

    expected_result = [clusters_with_leftovers_1, clusters_with_leftovers_3]
    assert result == expected_result


def test_remove_duplicates_with_continuous_measurements():
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()

    m1 = PseudoMeasurement(1, 1)
    m2 = PseudoMeasurement(2, 1)
    m3 = PseudoMeasurement(3, 1)
    m4 = PseudoMeasurement(4, 1)

    continuous1 = ContinuousMeasurement(measurements=[m1, m2])
    continuous2 = ContinuousMeasurement(measurements=[m3, m4])

    cluster1.add(continuous1)
    cluster2.add(continuous2)

    item1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m3, m4])
    item2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m3, m4])
    item3 = ClustersWithLeftovers(clusters=[cluster1, cluster2], leftovers=[])

    input_list = [item1, item2, item3]

    result = remove_duplicates(input_list)
    expected_result = [item1, item3]

    assert result == expected_result


def test_remove_duplicates_all_duplicates():
    cluster1 = MeasurementCluster()
    measurement1 = PseudoMeasurement(1, "a")

    cluster1.add(measurement1)

    item1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    item2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    item3 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    input_list = [item1, item2, item3]

    result = remove_duplicates(input_list)

    expected_result = [item1]
    assert result == expected_result


def test_remove_duplicates_identical_measurements_different_leftovers():
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()

    measurement1 = PseudoMeasurement(1, "a")
    measurement2 = PseudoMeasurement(2, "b")

    cluster1.add(measurement1)
    cluster2.add(measurement2)

    item1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement1])
    item2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[measurement2])
    item3 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[measurement2])
    input_list = [item1, item2, item3]

    result = remove_duplicates(input_list)

    expected_result = [item1, item2, item3]
    assert result == expected_result


def test_remove_duplicates_identical_continuous_different_core_measurements():
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    pseudo1, pseudo2 = PseudoMeasurement(1, 1), PseudoMeasurement(2, 1)
    continuous = ContinuousMeasurement(measurements=[pseudo1, pseudo2])
    core1 = PseudoMeasurement(3, "a")
    core2 = PseudoMeasurement(4, "b")

    cluster1.add(continuous)
    cluster1.add(core1)
    cluster2.add(continuous)
    cluster2.add(core2)

    item1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[])
    item2 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[])
    input_list = [item1, item2]

    result = remove_duplicates(input_list)

    expected_result = [item1, item2]
    assert result == expected_result
