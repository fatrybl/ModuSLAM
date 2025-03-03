from src.external.variants_factory import Factory
from src.measurement_storage.measurements.auxiliary import PseudoMeasurement
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import Imu, ImuData
from src.utils.auxiliary_objects import zero_vector3
from src.utils.ordered_set import OrderedSet


def test_create_with_empty_data():
    data: dict[type[Measurement], OrderedSet] = {}
    result = Factory.create(data, 0)
    assert result == []


def test_create_1_core():
    m1 = PseudoMeasurement(1, "a")
    ord_set = OrderedSet[PseudoMeasurement]()
    ord_set.add(m1)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set}

    result = Factory.create(data, 0)

    assert len(result) == 1

    comb1 = result[0]
    assert len(comb1.clusters) == 1
    assert len(comb1.leftovers) == 0
    assert m1 in comb1.clusters[0]


def test_create_1_imu():
    m1 = Imu(1, ImuData(zero_vector3, zero_vector3))
    ord_set = OrderedSet[Imu]()
    ord_set.add(m1)
    data: dict[type[Measurement], OrderedSet] = {Imu: ord_set}

    result = Factory.create(data, 0)

    assert result == []


def test_create_1_core_1_imu_before():
    m1 = Imu(1, ImuData(zero_vector3, zero_vector3))
    m2 = PseudoMeasurement(2, "a")
    ord_set1, ord_set2 = OrderedSet[Imu](), OrderedSet[PseudoMeasurement]()
    ord_set1.add(m1)
    ord_set2.add(m2)
    data: dict[type[Measurement], OrderedSet] = {Imu: ord_set1, PseudoMeasurement: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 1

    comb1 = result[0]

    assert len(comb1.clusters) == 1
    assert len(comb1.leftovers) == 0
    assert m2 in comb1.clusters[0]
    assert m1 in comb1.clusters[0].continuous_measurements[0].items


def test_create_1_core_1_imu_after():
    m1 = Imu(2, ImuData(zero_vector3, zero_vector3))
    m2 = PseudoMeasurement(1, "a")
    ord_set1, ord_set2 = OrderedSet[Imu](), OrderedSet[PseudoMeasurement]()
    ord_set1.add(m1)
    ord_set2.add(m2)
    data: dict[type[Measurement], OrderedSet] = {Imu: ord_set1, PseudoMeasurement: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 1

    combination = result[0]

    assert len(combination.clusters) == 1
    assert len(combination.leftovers) == 1
    assert m1 in combination.leftovers
    assert m2 in combination.clusters[0]
    assert combination.clusters[0].continuous_measurements == ()


def test_create_with_imu_measurements():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(3, "b")
    m3 = Imu(2, ImuData(zero_vector3, zero_vector3))
    ord_set1, ord_set2 = OrderedSet[PseudoMeasurement](), OrderedSet[Imu]()
    ord_set1.add(m1)
    ord_set1.add(m2)
    ord_set2.add(m3)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set1, Imu: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 2

    comb1, comb2 = result[0], result[1]

    assert len(comb1.clusters) == 2
    assert len(comb1.leftovers) == 0
    assert comb1.num_unused_measurements == 0
    assert m1 in comb1.clusters[0]
    assert m2 in comb1.clusters[1]
    assert m3 in comb1.clusters[1].continuous_measurements[0].items

    assert len(comb2.clusters) == 1
    assert len(comb2.leftovers) == 0
    assert comb2.num_unused_measurements == 1
    assert m1 in comb2.clusters[0]
    assert m2 in comb2.clusters[0]
    assert len(comb2.clusters[0].continuous_measurements) == 0


def test_create_with_core_measurements():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    ord_set = OrderedSet[PseudoMeasurement]()
    ord_set.add(m1)
    ord_set.add(m2)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set}

    result = Factory.create(data, 0)

    assert len(result) == 2
    comb1, comb2 = result[0], result[1]
    assert len(comb1.leftovers) == len(comb2.leftovers) == 0

    assert len(comb1.clusters) == 2
    assert m1 in comb1.clusters[0]
    assert m2 in comb1.clusters[1]
    assert m1 not in comb1.clusters[1]
    assert m2 not in comb1.clusters[0]

    assert len(comb2.clusters) == 1
    assert m1 in comb2.clusters[0]
    assert m2 in comb2.clusters[0]


def test_create_with_multiple_imu_measurements():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(3, "b")
    m3 = Imu(2, ImuData(zero_vector3, zero_vector3))
    m4 = Imu(4, ImuData(zero_vector3, zero_vector3))
    ord_set1, ord_set2 = OrderedSet[PseudoMeasurement](), OrderedSet[Imu]()
    ord_set1.add(m1)
    ord_set1.add(m2)
    ord_set2.add(m3)
    ord_set2.add(m4)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set1, Imu: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 2

    comb1, comb2 = result[0], result[1]

    assert len(comb1.clusters) == 2
    assert m4 in comb1.leftovers
    assert m3 in comb1.clusters[1].continuous_measurements[0].items
    assert m1 in comb1.clusters[0]
    assert m2 in comb1.clusters[1]
    assert m1 not in comb1.clusters[1]
    assert m2 not in comb1.clusters[0]

    assert len(comb2.clusters) == 1
    assert m4 in comb2.leftovers
    assert comb2.clusters[0].continuous_measurements == ()
    assert m1 in comb2.clusters[0]
    assert m2 in comb2.clusters[0]


def test_create_with_non_sequential_timestamps():
    m1 = PseudoMeasurement(3, "a")
    m2 = PseudoMeasurement(1, "b")
    m3 = Imu(2, ImuData(zero_vector3, zero_vector3))
    ord_set1, ord_set2 = OrderedSet[PseudoMeasurement](), OrderedSet[Imu]()
    ord_set1.add(m1)
    ord_set1.add(m2)
    ord_set2.add(m3)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set1, Imu: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 2

    comb1, comb2 = result[0], result[1]

    assert len(comb1.clusters) == 2
    assert len(comb1.leftovers) == 0
    assert m2 in comb1.clusters[0]
    assert m1 in comb1.clusters[1]
    assert m3 in comb1.clusters[1].continuous_measurements[0].items

    assert len(comb2.clusters) == 1
    assert len(comb2.leftovers) == 0
    assert m2 in comb2.clusters[0]
    assert m1 in comb2.clusters[0]
    assert comb2.clusters[0].continuous_measurements == ()
    assert comb2.num_unused_measurements == 1


def test_create_with_2_imu_between_core():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(4, "b")
    m3 = Imu(2, ImuData(zero_vector3, zero_vector3))
    m4 = Imu(3, ImuData(zero_vector3, zero_vector3))
    ord_set1, ord_set2 = OrderedSet[PseudoMeasurement](), OrderedSet[Imu]()
    ord_set1.add(m1)
    ord_set1.add(m2)
    ord_set2.add(m3)
    ord_set2.add(m4)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set1, Imu: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 2

    comb1, comb2 = result[0], result[1]

    assert len(comb1.clusters) == 2
    assert len(comb1.leftovers) == 0
    assert m1 in comb1.clusters[0]
    assert m2 in comb1.clusters[1]
    assert m3 in comb1.clusters[1].continuous_measurements[0].items
    assert m4 in comb1.clusters[1].continuous_measurements[0].items

    assert len(comb2.clusters) == 1
    assert len(comb2.leftovers) == 0
    assert m1 in comb2.clusters[0]
    assert m2 in comb2.clusters[0]
    assert comb2.clusters[0].continuous_measurements == ()
    assert comb2.num_unused_measurements == 2


def test_create_with_2_imu_out():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = Imu(2, ImuData(zero_vector3, zero_vector3))
    m4 = Imu(3, ImuData(zero_vector3, zero_vector3))
    ord_set1, ord_set2 = OrderedSet[PseudoMeasurement](), OrderedSet[Imu]()
    ord_set1.add(m1)
    ord_set1.add(m2)
    ord_set2.add(m3)
    ord_set2.add(m4)
    data: dict[type[Measurement], OrderedSet] = {PseudoMeasurement: ord_set1, Imu: ord_set2}

    result = Factory.create(data, 0)

    assert len(result) == 2

    comb1, comb2 = result[0], result[1]

    assert len(comb1.clusters) == 2
    assert len(comb1.leftovers) == 2
    assert m1 in comb1.clusters[0]
    assert m2 in comb1.clusters[1]
    assert comb1.clusters[0].continuous_measurements == ()
    assert comb1.clusters[1].continuous_measurements == ()
    assert m3 in comb1.leftovers
    assert m4 in comb1.leftovers

    assert len(comb2.clusters) == 1
    assert len(comb2.leftovers) == 2
    assert m1 in comb2.clusters[0]
    assert m2 in comb2.clusters[0]
    assert comb2.clusters[0].continuous_measurements == ()
    assert m3 in comb2.leftovers
    assert m4 in comb2.leftovers
    assert comb2.num_unused_measurements == 0
