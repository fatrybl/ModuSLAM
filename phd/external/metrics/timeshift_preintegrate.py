from collections.abc import Sequence

from phd.external.metrics.protocols import Metrics
from phd.external.objects.auxiliary_objects import Connection
from phd.external.objects.measurements_cluster import Cluster


class TotalTimeShift(Metrics):

    @classmethod
    def compute(cls) -> int:
        """Sum of time shifts of the measurements.

        Args:
            graph: graph to compute metrics for.

            measurements: pre-integrate measurements.

        Returns:
            metrics value.
        """

        # vertices_time_shift = cls._accumulative_time_shift_vertices(graph.vertices)
        # edges_time_shift = cls._accumulative_time_shift_edges(graph.edges, measurements)
        # total = vertices_time_shift + edges_time_shift
        # return total
        raise NotImplementedError

    @classmethod
    def _accumulative_time_shift_vertices(cls, vertices: list[Cluster]) -> int:
        # """Calculates accumulative time shift for the merged vertices.
        #
        # Args:
        #     vertices: vertices with merged measurements.
        #
        # Returns:
        #     accumulative times shift.
        # """
        # total_shift = 0
        #
        # for vertex in vertices:
        #     median_value = median(vertex.measurements)
        #     total_shift += sum_of_differences(vertex.measurements, median_value)
        #
        # return total_shift
        raise NotImplementedError

    @classmethod
    def _accumulative_time_shift_edges(
        cls, edges: list[Connection], timestamps: Sequence[int]
    ) -> int:
        # """Calculates accumulative time shift for edges using a sequence of timestamps.
        #
        # Args:
        #     edges: edges to calculate a time shift for.
        #
        #     timestamps: timestamps of edges` measurements.
        #
        # Returns:
        #     accumulative times shift.
        # """
        #
        # total = 0
        # for edge in edges:
        #     v1_timestamp = median(edge.vertex1.measurements)
        #     t_imu_start = cls._get_right_closest_timestamps(timestamps, v1_timestamp)
        #     if t_imu_start:
        #         total += abs(t_imu_start - v1_timestamp)
        #
        # return total
        raise NotImplementedError

    @staticmethod
    def _get_right_closest_timestamps(timestamps: Sequence[int], limit: int) -> int | None:
        """Gets right closes timestamp in the sequence.

        Args:
            limit: timestamp limit.

            timestamps: sequence of timestamps to find a closest element in.

        Returns:
            right closest element in the sequence.
        """
        return next((t for t in timestamps if t >= limit), None)


if __name__ == "__main__":
    # v1 = Vertex((1,))
    # v2 = Vertex((7, 9, 11))
    # v3 = Vertex((15,))
    #
    # e1 = Edge(vertex1=v1, vertex2=v3)
    #
    # measurements = [0, 1, 2, 4, 6, 8, 10, 12, 13, 14]
    #
    # graph = Graph(vertices=[v1, v2, v3], edges=[e1])
    #
    # total_time_shift = TotalTimeShift.compute(graph, measurements)
    # print(f"Total Time Shift: {total_time_shift}")
    ...
