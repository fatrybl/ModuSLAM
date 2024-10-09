from phd.external.metrics.protocols import Metrics


class TotalTimeShift(Metrics):

    @classmethod
    def compute(cls) -> int:
        """Sum of time shifts of the measurements.

        Returns:
            metrics value.
        """
        raise NotImplementedError

    #
    # @staticmethod
    # def _accumulative_time_shift_vertices(clusters: list[Cluster]) -> int:
    #     """Calculates accumulative time shift for the merged vertices.
    #
    #     Args:
    #         clusters: clusters with measurements.
    #
    #     Returns:
    #         accumulative times shift.
    #     """
    #     total_shift = 0
    #
    #     for cluster in clusters:
    #         median_value = median(cluster)
    #         total_shift += sum_of_differences(cluster.measurements, median_value)
    #
    #     return total_shift


if __name__ == "__main__":
    ...
