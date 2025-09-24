from moduslam.external.combinations_factory import Factory
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.group import MeasurementGroup
from moduslam.measurement_storage.measurements.auxiliary import PseudoMeasurement


def test_combine_with_empty_iterable():
    result = Factory.combine([])
    assert result == [[]], "Expected an empty list when input is an empty iterable"


def test_combine_with_single_measurement_group():
    measurement = PseudoMeasurement(1, "a")
    group = MeasurementGroup()
    group.add(measurement)

    result = Factory.combine([group])

    assert len(result) == 1
    assert len(result[0]) == 1
    assert len(result[0][0].measurements) == 1
    assert result[0][0].measurements[0] == measurement


def test_combine_with_multiple_measurement_groups():
    measurement1 = PseudoMeasurement(1, "a")
    measurement2 = PseudoMeasurement(2, "b")
    measurement3 = PseudoMeasurement(3, "c")

    group1, group2, group3 = MeasurementGroup(), MeasurementGroup(), MeasurementGroup()

    group1.add(measurement1)
    group2.add(measurement2)
    group3.add(measurement3)

    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()
    cluster1.add(measurement1)
    cluster2.add(measurement2)
    cluster3.add(measurement3)

    comb1 = [cluster1, cluster2, cluster3]

    cluster = MeasurementCluster()
    cluster.add(measurement1)
    cluster.add(measurement2)
    cluster.add(measurement3)

    comb2 = [cluster]

    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(measurement1)
    cluster2.add(measurement2)
    cluster2.add(measurement3)

    comb3 = [cluster1, cluster2]

    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(measurement1)
    cluster1.add(measurement2)
    cluster2.add(measurement3)

    comb4 = [cluster1, cluster2]

    expected_combinations = [comb1, comb2, comb3, comb4]

    result = Factory.combine([group1, group2, group3])

    assert len(result) == len(expected_combinations)

    for clusters in result:
        found_match = False

        for expected_clusters in expected_combinations:

            if len(clusters) == len(expected_clusters) and all(
                result_cluster.measurements == expected_cluster.measurements
                for result_cluster, expected_cluster in zip(clusters, expected_clusters)
            ):
                found_match = True
                break

        assert found_match is True


def test_combine_correctly_merge_adjacent_groups():
    measurement1 = PseudoMeasurement(1, "a")
    measurement2 = PseudoMeasurement(2, "b")
    measurement3 = PseudoMeasurement(3, "c")

    group1, group2, group3 = MeasurementGroup(), MeasurementGroup(), MeasurementGroup()
    group1.add(measurement1)
    group2.add(measurement2)
    group3.add(measurement3)

    result = Factory.combine([group1, group2, group3])

    assert len(result) == 4, "Expected 4 combinations"

    expected_cluster = MeasurementCluster()
    expected_cluster.add(measurement1)
    expected_cluster.add(measurement2)
    expected_cluster.add(measurement3)

    found_expected = any(
        len(clusters) == 1 and clusters[0].measurements == expected_cluster.measurements
        for clusters in result
    )

    assert (
        found_expected
    ), "Expected a combination where all measurements are merged into one cluster"


def test_combine_with_empty_measurement_groups():
    group1, group2 = MeasurementGroup(), MeasurementGroup()

    result = Factory.combine([group1, group2])

    for clusters in result:
        for cluster in clusters:
            assert cluster.empty is True
