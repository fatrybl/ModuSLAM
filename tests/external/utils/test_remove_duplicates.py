import pytest

from moduslam.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from moduslam.external.utils import remove_duplicates
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import PseudoMeasurement
from moduslam.measurement_storage.measurements.continuous import ContinuousMeasurement
from moduslam.measurement_storage.measurements.imu import Imu, ImuData
from moduslam.utils.auxiliary_objects import zero_vector3


@pytest.fixture
def data() -> ImuData:
    """Zeroed ImuData object."""
    return ImuData(zero_vector3, zero_vector3)


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


def test_remove_duplicates_with_identical_measurements_and_leftovers(data: ImuData):
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    m1, m2 = Imu(1, data), Imu(2, data)

    cluster1.add(m1)
    cluster2.add(m2)

    clusters_with_leftovers_1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m1])
    clusters_with_leftovers_2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m1])
    clusters_with_leftovers_3 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[m2])
    input_list = [clusters_with_leftovers_1, clusters_with_leftovers_2, clusters_with_leftovers_3]

    result = remove_duplicates(input_list)

    expected_result = [clusters_with_leftovers_1, clusters_with_leftovers_3]
    assert result == expected_result


def test_remove_duplicates_with_continuous_measurements(data: ImuData):
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    m1, m2 = Imu(1, data), Imu(2, data)
    m3, m4 = Imu(3, data), Imu(4, data)
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


def test_remove_duplicates_all_duplicates(data: ImuData):
    cluster = MeasurementCluster()
    m = Imu(1, data)

    cluster.add(m)

    item1 = ClustersWithLeftovers(clusters=[cluster], leftovers=[m])
    item2 = ClustersWithLeftovers(clusters=[cluster], leftovers=[m])
    item3 = ClustersWithLeftovers(clusters=[cluster], leftovers=[m])
    input_list = [item1, item2, item3]

    result = remove_duplicates(input_list)

    expected_result = [item1]
    assert result == expected_result


def test_remove_duplicates_identical_measurements_different_leftovers(data: ImuData):
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    m1, m2 = Imu(1, data), Imu(2, data)

    cluster1.add(m1)
    cluster2.add(m2)

    item1 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m1])
    item2 = ClustersWithLeftovers(clusters=[cluster1], leftovers=[m2])
    item3 = ClustersWithLeftovers(clusters=[cluster2], leftovers=[m2])
    input_list = [item1, item2, item3]

    result = remove_duplicates(input_list)

    expected_result = [item1, item2, item3]
    assert result == expected_result


def test_remove_duplicates_identical_continuous_different_core_measurements(data: ImuData):
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    m1, m2 = Imu(1, data), Imu(2, data)
    continuous = ContinuousMeasurement(measurements=[m1, m2])
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
