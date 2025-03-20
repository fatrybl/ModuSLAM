from src.bridge.auxiliary_dataclasses import Connection
from src.external.metrics.connection_consistency import EdgeConsistency
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.auxiliary import PseudoMeasurement
from src.measurement_storage.measurements.continuous import ContinuousMeasurement


def test_edge_consistency_correct():
    d1 = PseudoMeasurement(1, "a")
    d2 = PseudoMeasurement(4, "b")
    d3 = PseudoMeasurement(7, "c")

    m1 = PseudoMeasurement(1, 1)
    m2 = PseudoMeasurement(2, 1)
    m3 = PseudoMeasurement(5, 1)
    measurement = ContinuousMeasurement(measurements=[m1, m2, m3])

    c1, c2, c3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()

    c1.add(d1)
    c2.add(d2)
    c3.add(d3)

    con1, con2 = Connection(c1, c2), Connection(c2, c3)
    connections = [con1, con2]

    status = EdgeConsistency.compute(connections, measurement)
    assert status is True


def test_edge_consistency_incorrect():
    d1 = PseudoMeasurement(1, "a")
    d2 = PseudoMeasurement(4, "b")

    m1 = PseudoMeasurement(4, 1)
    m2 = PseudoMeasurement(5, 1)
    m3 = PseudoMeasurement(6, 1)

    measurement = ContinuousMeasurement(measurements=[m1, m2, m3])

    c1, c2 = MeasurementCluster(), MeasurementCluster()

    c1.add(d1)
    c2.add(d2)

    connections = [Connection(c1, c2)]

    status = EdgeConsistency.compute(connections, measurement)

    assert status is False


def test_edge_consistency_no_measurements():
    d1 = PseudoMeasurement(1, "a")
    d2 = PseudoMeasurement(2, "b")

    m1 = PseudoMeasurement(3, 1)

    measurement = ContinuousMeasurement(measurements=[m1])

    c1, c2 = MeasurementCluster(), MeasurementCluster()

    c1.add(d1)
    c2.add(d2)

    connections = [Connection(c1, c2)]

    status = EdgeConsistency.compute(connections, measurement)

    assert status is False


def test_edge_consistency_single_measurement():
    d1 = PseudoMeasurement(1, "a")
    d2 = PseudoMeasurement(4, "b")

    m1 = PseudoMeasurement(2, 1)
    measurement = ContinuousMeasurement(measurements=[m1])

    c1, c2 = MeasurementCluster(), MeasurementCluster()

    c1.add(d1)
    c2.add(d2)

    connections = [Connection(c1, c2)]

    status = EdgeConsistency.compute(connections, measurement)

    assert status is True
