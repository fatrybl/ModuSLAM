from phd_thesis.src.metrics.protocols import Metrics
from phd_thesis.src.metrics.utils import median, sum_of_differences
from phd_thesis.src.objects import Graph, Vertex


class TotalTimeShift(Metrics):

    @classmethod
    def compute(cls, graph: Graph) -> int:
        """Sum of time shifts of the measurements.

        Args:
            graph: graph to compute metrics for.

        Returns:
            metrics value.
        """

        time_shift = cls._accumulative_time_shift_vertices(graph.vertices)
        return time_shift

    @staticmethod
    def _accumulative_time_shift_vertices(vertices: list[Vertex]) -> int:
        """Calculates accumulative time shift for the merged vertices.

        Args:
            vertices: vertices with merged measurements.

        Returns:
            accumulative times shift.
        """
        total_shift = 0

        for vertex in vertices:
            median_value = median(vertex.measurements)
            total_shift += sum_of_differences(vertex.measurements, median_value)

        return total_shift


# v1 = Vertex((1, 2, 3))
# v2 = Vertex((4, 7, 8))
# v3 = Vertex((3,))
#
# e1 = Edge(vertex1=v1, vertex2=v2)
# e2 = Edge(vertex1=v2, vertex2=v3)
#
# graph = Graph(vertices=[v1, v2, v3], edges=[e1, e2])
#
# total_time_shift = TotalTimeShift.compute(graph)
# print(f"Total Time Shift: {total_time_shift}")
