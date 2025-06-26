from dataclasses import dataclass

from src.moduslam.map_manager.visualizers.graph_visualizer.visualizer_params import (
    ClusterParams,
)
from src.utils.auxiliary_dataclasses import Position2D, TimeRange
from src.utils.auxiliary_methods import nanosec2sec


@dataclass(frozen=True, eq=True)
class Vertex:
    """A graph vertex for visualization.

    Args:
        index: a vertex ID
        label: a label of the vertex.
        radius: a circle radius for the vertex.
    """

    index: int
    label: str
    radius: float = 50.0

    def __repr__(self) -> str:
        return self.label + str(self.index)


class Cluster:
    """A cluster of vertices for visualization."""

    def __init__(
        self,
        index: int,
        time_range: TimeRange,
        position: Position2D = Position2D(0, 0),
        visual_params: ClusterParams = ClusterParams(),
    ):
        """
        Args:
            index: a cluster ID.

            time_range: a time range of the cluster.

            position: a 2D position of the cluster.

            visual_params: visualization parameters for the cluster.
        """
        self._label = "C"
        self._index = index
        self._position = position
        self._time_range = time_range
        self._width = visual_params.width
        self._height = visual_params.height
        self._width_step = visual_params.width_step
        self._vertices: dict[Vertex, Position2D] = {}

    @property
    def time_range(self) -> str:
        """Time range of the cluster."""
        t_range = self._time_range
        dt = nanosec2sec(t_range.stop - t_range.start)
        delta = "\u0394"
        return f"{delta}T, s: {dt:.1f}"

    @property
    def top_center(self) -> Position2D:
        """Top center position of the cluster."""
        x = self._position.x + self.width / 2
        y = self._position.y + self._height
        return Position2D(x, y)

    @property
    def bottom_center(self) -> Position2D:
        """Bottom center position of the cluster."""
        x = self._position.x + self.width / 2
        y = self._position.y
        return Position2D(x, y)

    @property
    def label(self) -> str:
        """Cluster label."""
        return self._label + str(self._index)

    @property
    def vertices_with_positions(self) -> dict[Vertex, Position2D]:
        """Vertices of the cluster with their positions."""
        return self._vertices

    @property
    def vertices(self) -> list[Vertex]:
        """Vertices of the cluster."""
        return list(self._vertices.keys())

    @property
    def position(self) -> Position2D:
        """2D position of the cluster."""
        return self._position

    @property
    def height(self) -> float:
        """Height of the cluster."""
        return self._height

    @property
    def width(self) -> float:
        """The width of the cluster based on the number of vertices.

        0 if no vertices are present.
        """
        return len(self._vertices) * self._width_step

    def set_position(self, position: Position2D) -> None:
        """Sets a new position for the cluster."""
        dp = Position2D(position.x - self._position.x, position.y - self._position.y)
        self._position = position
        self._update_vertices_positions(dp)

    def add(self, vertex: Vertex) -> None:
        """Adds a new vertex to the cluster."""
        position = self._calculate_position()
        self._vertices[vertex] = position

    def _calculate_position(self) -> Position2D:
        """Calculates the position of a new vertex in the cluster.

        Returns:
            a position for a new vertex.
        """
        x = self._position.x + self.width + self._width_step / 2
        y = self._position.y + self._height / 2
        return Position2D(x, y)

    def _update_vertices_positions(self, dp: Position2D) -> None:
        """Updates the positions of all vertices in the cluster."""
        for vertex, current_position in self._vertices.items():
            current_position.x += dp.x
            current_position.y += dp.y

    def __repr__(self) -> str:
        return f"{self._label + str(self._index)}"


if __name__ == "__main__":
    v, p, b = Vertex(1, "V"), Vertex(1, "P"), Vertex(1, "B")
    c = Cluster(0, TimeRange(0, 1))

    for vertex in [v, p, b]:
        c.add(vertex)

    for vertex, pose in c.vertices_with_positions.items():
        print(vertex, pose)

    c.set_position(Position2D(5, 0))

    for vertex, pose in c.vertices_with_positions.items():
        print(vertex, pose)
