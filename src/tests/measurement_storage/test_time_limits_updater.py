from src.measurement_storage.measurements.auxiliary import FakeMeasurement
from src.measurement_storage.measurements.base import TimeRangeMeasurement
from src.measurement_storage.measurements.time_limits_updater import Updater
from src.utils.auxiliary_dataclasses import TimeRange


class FakeTimeRangeMeasurement(FakeMeasurement, TimeRangeMeasurement):
    def __init__(self, start: int, stop: int):
        super().__init__(stop)
        self._t_range = TimeRange(start, stop)

    @property
    def time_range(self) -> TimeRange:
        return self._t_range


def test_update_start_stop_on_adding():
    t1, t2 = 0, 1
    initial_start = initial_stop = t1
    measurement = FakeMeasurement(t2)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == t1
    assert updated_stop == t2


def test_update_start_stop_on_adding_with_time_range_measurement():
    t1, t2 = 5, 10
    initial_start, initial_stop = 6, 9
    measurement = FakeTimeRangeMeasurement(t1, t2)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == t1
    assert updated_stop == t2


def test_update_start_stop_on_adding_with_time_range_within_initial():
    t1, t2 = 6, 10
    initial_start, initial_stop = 5, 15
    measurement = FakeTimeRangeMeasurement(t1, t2)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == initial_start
    assert updated_stop == initial_stop


def test_update_start_when_time_range_measurement_start_earlier_than_initial_start():
    initial_start, initial_stop = 10, 20
    measurement_start, measurement_stop = 5, 15
    measurement = FakeTimeRangeMeasurement(measurement_start, measurement_stop)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == measurement_start
    assert updated_stop == initial_stop


def test_update_stop_when_time_range_measurement_stop_later_than_initial_stop():
    t1, t2 = 6, 15
    initial_start, initial_stop = 5, 10
    measurement = FakeTimeRangeMeasurement(t1, t2)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == initial_start
    assert updated_stop == t2


def test_update_start_stop_on_adding_with_simple_measurement():
    t = 5
    initial_start, initial_stop = 10, 20
    measurement = FakeMeasurement(t)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == t
    assert updated_stop == initial_stop


def test_no_change_when_simple_measurement_within_initial_range():
    t = 10
    initial_start, initial_stop = 5, 15
    measurement = FakeMeasurement(t)

    updated_start, updated_stop = Updater.update_start_stop_on_adding(
        measurement, initial_start, initial_stop
    )

    assert updated_start == initial_start
    assert updated_stop == initial_stop
