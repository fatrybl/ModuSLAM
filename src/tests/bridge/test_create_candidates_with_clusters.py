from src.bridge.candidates_factory import create_candidates_with_clusters
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import ContinuousImu, ProcessedImu
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.ordered_set import OrderedSet


def test_1(measurement: ContinuousImu[ProcessedImu]):
    graph = Graph()
    o_set1 = OrderedSet[PoseMeasurement]()
    o_set2 = OrderedSet[ProcessedImu]()
    m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(3, i4x4, i3x3, i3x3)

    for item in measurement.items:
        o_set2.add(item)

    o_set1.add(m1)
    o_set1.add(m2)

    data: dict[type[Measurement], OrderedSet] = {PoseMeasurement: o_set1, ProcessedImu: o_set2}

    items = create_candidates_with_clusters(graph, data)

    assert len(items) == 2

    can1, can2 = items

    assert len(can1.clusters) == 2
    assert len(can2.clusters) == 1

    assert can1.candidate.leftovers == []
    assert can2.candidate.leftovers == []
    assert can1.candidate.num_unused_measurements == 0
    assert can2.candidate.num_unused_measurements == 3
