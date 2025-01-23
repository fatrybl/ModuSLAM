import pytest

from src.bridge.candidates_factory import create_candidates_with_clusters
from src.external.metrics.factory import MetricsFactory
from src.external.metrics.storage import MetricsStorage
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import (
    ImuCovariance,
    ImuData,
    ProcessedImu,
)
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.measurement_storage.measurements.position import Position
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.auxiliary_objects import zero_vector3
from src.utils.exceptions import ItemNotExistsError
from src.utils.ordered_set import OrderedSet


def get_best_candidate(storage: MetricsStorage):
    """Chooses the best candidate based on the timeshift.

    Args:
        storage: a storage with metrics.

    Returns:
        the best candidate.

    Raises:
        ItemNotExistsError: if no best candidate exists.
    """
    table = storage.get_timeshift_table()
    candidates = sorted(table, key=lambda k: table[k])
    for candidate in candidates:
        connectivity = storage.get_connectivity_status(candidate)
        if connectivity:
            return candidate

    raise ItemNotExistsError("No best candidate exists.")


@pytest.fixture
def data1() -> dict[type[Measurement], OrderedSet]:
    """1-st data sequence."""
    # IMU timestamps
    i1 = 1544677152007481210
    i2 = 1544677152017477733
    i3 = 1544677152027474993
    i4 = 1544677152037471897
    i5 = 1544677152047475379
    i6 = 1544677152057526255
    i7 = 1544677152067477872
    i8 = 1544677152077478461
    i9 = 1544677152087520272
    i10 = 1544677152097472327
    i11 = 1544677152107486048
    i12 = 1544677152117474402
    i13 = 1544677152127479938
    i14 = 1544677152137478140
    i15 = 1544677152147516195

    # Core timestamps
    t1 = 1544677152006678000
    t2 = 1544677152051931000
    t3 = 1544677152107529000
    t4 = 1544677152152812000

    o1 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)
    o2 = Odometry(t4, TimeRange(t2, t4), i4x4, i3x3, i3x3)

    pose = Position(t1, zero_vector3, i3x3)

    imu_data = ImuData(zero_vector3, zero_vector3)
    covariance = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
    imu_measurements = [
        ProcessedImu(t, imu_data, covariance, i4x4)
        for t in [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15]
    ]

    o_set1, o_set2, o_set3 = (
        OrderedSet[Odometry](),
        OrderedSet[ProcessedImu](),
        OrderedSet[Position](),
    )
    o_set1.add(o1)
    o_set1.add(o2)
    o_set3.add(pose)
    for m in imu_measurements:
        o_set2.add(m)

    data: dict[type[Measurement], OrderedSet] = {
        Odometry: o_set1,
        ProcessedImu: o_set2,
        Position: o_set3,
    }
    return data


@pytest.fixture
def data2() -> dict[type[Measurement], OrderedSet]:
    """2-nd data sequence."""

    # IMU timestamps
    i1 = 1544677152157475234
    i2 = 1544677152167471209
    i3 = 1544677152177470704
    i4 = 1544677152187473028
    i5 = 1544677152197513728
    i6 = 1544677152207498590
    i7 = 1544677152217476695
    i8 = 1544677152227476247
    i9 = 1544677152237479703
    i10 = 1544677152247485900

    # Core timestamps
    t3 = 1544677152107529000
    t4 = 1544677152152812000
    t5 = 1544677152208367000
    t6 = 1544677152213135689
    t7 = 1544677152253673000

    o3 = Odometry(t5, TimeRange(t3, t5), i4x4, i3x3, i3x3)
    pos = Position(t6, zero_vector3, i3x3)
    o4 = Odometry(t7, TimeRange(t4, t7), i4x4, i3x3, i3x3)

    imu_data = ImuData(zero_vector3, zero_vector3)
    covariance = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
    imu_measurements = [
        ProcessedImu(t, imu_data, covariance, i4x4)
        for t in [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10]
    ]

    o_set1 = OrderedSet[Odometry]()
    o_set2 = OrderedSet[Position]()
    o_set3 = OrderedSet[ProcessedImu]()
    o_set1.add(o3)
    o_set1.add(o4)
    o_set2.add(pos)
    for m in imu_measurements:
        o_set3.add(m)

    data: dict[type[Measurement], OrderedSet] = {
        Odometry: o_set1,
        Position: o_set2,
        ProcessedImu: o_set3,
    }
    return data


@pytest.fixture
def graph(data1: dict[type[Measurement], OrderedSet]) -> Graph:
    """A graph created from the 1-st data sequence."""
    graph = Graph()
    storage = MetricsStorage()

    variants = create_candidates_with_clusters(graph, data1)

    for var in variants:
        timeshift = MetricsFactory.compute_timeshift(var.clusters)
        connectivity = MetricsFactory.compute_connectivity(var.candidate)
        storage.add_timeshift(var.candidate, timeshift)
        storage.add_connectivity(var.candidate, connectivity)

    best = get_best_candidate(storage)
    return best.graph


def test_1(graph: Graph, data2: dict[type[Measurement], OrderedSet]):
    items = create_candidates_with_clusters(graph, data2)
    assert len(items) == 8
