from collections.abc import Iterable

from src.external.metrics.base import Metrics
from src.measurement_storage.cluster import MeasurementCluster


class TimeShift(Metrics):

    @classmethod
    def compute(cls, clusters: Iterable[MeasurementCluster]) -> int:
        """Calculates the accumulative time shift for the clusters.

        Args:
            clusters: clusters with measurements.

        Returns:
            accumulative times shift.
        """
        time_shift: int = 0

        for cluster in clusters:
            start, stop = cluster.time_range.start, cluster.time_range.stop
            time_shift += stop - start

            # compute for continuous separately as it is not counted in cluster`s time_range.
            # only left border is taken into account.
            for m in cluster.continuous_measurements:
                first = m.items[0].timestamp
                start = m.time_range.start
                time_shift += first - start

        return time_shift
