from src.measurement_storage.measurements.base import Measurement, TimeRangeMeasurement
from src.utils.ordered_set import OrderedSet


class Updater:
    @staticmethod
    def update_start_stop_on_adding(
        measurement: Measurement, start: int | None, stop: int | None
    ) -> tuple[int, int]:
        """Calculates new start & stop timestamps when the measurement is added.

        Args:
            measurement: a measurement to update the time range with.

            start: a start timestamp to update.

            stop: the new stop timestamp.
        """
        if isinstance(measurement, TimeRangeMeasurement):
            m_start, m_stop = measurement.time_range.start, measurement.time_range.stop
            start = m_start if start is None or m_start < start else start
            stop = m_stop if stop is None or m_stop > stop else stop
        else:
            t = measurement.timestamp
            start = t if start is None or t < start else start
            stop = t if stop is None or t > stop else stop

        return start, stop

    @classmethod
    def update_start_stop_on_removing(
        cls,
        data: dict[type[Measurement], OrderedSet[Measurement]],
        removable: Measurement,
        start: int | None,
        stop: int | None,
    ) -> tuple[int | None, int | None]:
        """Calculates new start & stop timestamps when the measurement is removed.

        Args:
            data: a dictionary with measurements.

            removable: a measurement being removed.

            start: current start timestamp to update.

            stop: current stop timestamp to update.

        Returns:
            updated timestamps.
        """
        if not data:
            return None, None

        if cls._is_start_timestamp_affected(start, removable):
            start = cls._get_min_timestamp(data)

        if cls._is_stop_timestamp_affected(stop, removable):
            stop = cls._get_max_timestamp(data)

        return start, stop

    @staticmethod
    def _get_min_timestamp(data: dict[type[Measurement], OrderedSet[Measurement]]) -> int | None:
        """Returns the minimum timestamp from all measurements.
        Complexity: O(n**2)

        Args:
            data: a dictionary with measurements.

        Returns:
            minimum timestamp from all measurements.
        """
        start = None
        for m_set in data.values():
            for measurement in m_set:
                if isinstance(measurement, TimeRangeMeasurement):
                    current_start = measurement.time_range.start
                else:
                    current_start = measurement.timestamp

                start = current_start if start is None or current_start < start else start

        return start

    @staticmethod
    def _get_max_timestamp(data: dict[type[Measurement], OrderedSet[Measurement]]) -> int | None:
        """Returns the maximum timestamp from all measurements.
        Complexity: O(n**2)

        Args:
            data: a dictionary with measurements.

        Returns:
            maximum timestamp from all measurements.
        """
        stop = None
        for m_set in data.values():
            for measurement in m_set:
                if isinstance(measurement, TimeRangeMeasurement):
                    current_stop = measurement.time_range.stop
                else:
                    current_stop = measurement.timestamp

                stop = current_stop if stop is None or current_stop > stop else stop

        return stop

    @staticmethod
    def _is_start_timestamp_affected(start: int | None, measurement: Measurement) -> bool:
        """Checks if the start timestamp is affected by the removing measurement."""
        if isinstance(measurement, TimeRangeMeasurement):
            return measurement.time_range.start == start
        else:
            return measurement.timestamp == start

    @staticmethod
    def _is_stop_timestamp_affected(stop: int | None, measurement: Measurement) -> bool:
        """Checks if the stop timestamp is affected by the removing measurement."""
        if isinstance(measurement, TimeRangeMeasurement):
            return measurement.time_range.stop == stop
        else:
            return measurement.timestamp == stop
