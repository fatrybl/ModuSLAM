import logging
from collections.abc import Iterable
from typing import Generic, overload

import gtsam
from plum import dispatch

from slam.frontend_manager.graph.base_vertices import (
    GraphVertex,
    NotOptimizableVertex,
    OptimizableVertex,
    Vertex,
)
from slam.frontend_manager.graph.custom_vertices import (
    CameraFeature,
    ImuBias,
    LidarPose,
    NavState,
    Pose,
    Velocity,
)
from slam.frontend_manager.graph.index_generator import IndexStorage
from slam.utils.deque_set import DequeSet
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class VertexStorage(Generic[GraphVertex]):
    """Stores vertices of the Graph."""

    def __init__(self):
        self._vertices = DequeSet[GraphVertex]()
        self._index_storage = IndexStorage()

        self._optimizable_vertices = OrderedSet[OptimizableVertex]()
        self._not_optimizable_vertices = OrderedSet[NotOptimizableVertex]()

        self._vertices_table: dict[type[Vertex], DequeSet] = {
            Pose: DequeSet[Pose](),
            Velocity: DequeSet[Velocity](),
            NavState: DequeSet[NavState](),
            ImuBias: DequeSet[ImuBias](),
            LidarPose: DequeSet[LidarPose](),
            CameraFeature: DequeSet[CameraFeature](),
        }

    @property
    def index_storage(self) -> IndexStorage:
        return self._index_storage

    @property
    def vertices(self) -> DequeSet[GraphVertex]:
        """All vertices in the Graph.

        Returns:
            all vertices in the graph (DequeSet[GraphVertex]).
        """
        return self._vertices

    @property
    def optimizable_vertices(self) -> OrderedSet[OptimizableVertex]:
        """Optimizable vertices in the Graph.

        Returns:
            optimizable vertices in the graph (OrderedSet[OptimizableVertex]).
        """
        return self._optimizable_vertices

    @property
    def not_optimizable_vertices(self) -> OrderedSet[NotOptimizableVertex]:
        """Vertices which are not being optimized in the graph. They are not variables
        and are not being included in GTSAM factors directly.

        Returns:
            constant vertices in the graph (OrderedSet[NotOptimizableVertex]).
        """
        return self._not_optimizable_vertices

    def get_vertices(self, vertex_type: type[Vertex]) -> DequeSet:
        """Returns vertices of the given type.

        Args:
            vertex_type (type[GraphVertex]): type of the vertices.

        Returns:
            (DequeSet): vertices of the given type.
        """
        if vertex_type not in self._vertices_table:
            raise KeyError(f"Type {vertex_type!r} has not been defined in the vertices table.")
        else:
            return self._vertices_table[vertex_type]

    @overload
    def add(self, vertex: GraphVertex) -> None:
        """
        @overload.
        Adds new vertex based on its type.
        Args:
            vertex (GraphVertex): new vertex to be added to the graph.
        """
        self._index_storage.add(vertex.index)
        self._vertices.add(vertex)
        self._add_to_table(vertex)
        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.add(vertex)
        elif isinstance(vertex, NotOptimizableVertex):
            self._not_optimizable_vertices.add(vertex)
        else:
            msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NotOptimizable."
            logger.critical(msg)
            raise TypeError(msg)

    @overload
    def add(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.
        Adds new vertices to collections based on its type.
        Args:
            vertices (Iterable[GraphVertex]): new vertices to be added to the graph.
        """
        [self.add(v) for v in vertices]

    @dispatch
    def add(self, vertex=None):
        """
        @overload.

        Adds new vertex(s) to the graph.

        Calls:
            1.  add single vertex to the graph.
                Args:
                    vertex (GraphVertex): new vertex to be added to the graph.

            2.  add multiple vertices to the graph.
                Args:
                    vertices (Iterable[GraphVertex]): new vertices to be added to the graph.
        """

    @overload
    def remove(self, vertex: GraphVertex) -> None:
        """
        @overload.
        Removes vertex from the graph.
        Args:
            vertex (GraphVertex): a vertex to be removed from the graph.
        """
        self._index_storage.remove(vertex.index)
        self._vertices.remove(vertex)
        self._remove_from_table(vertex)
        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.remove(vertex)
        elif isinstance(vertex, NotOptimizableVertex):
            self._not_optimizable_vertices.remove(vertex)
        else:
            msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NotOptimizable."
            logger.critical(msg)
            raise TypeError(msg)

    @overload
    def remove(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.
        Removes multiple vertices from the graph.
        Args:
            vertices (Iterable[GraphVertex]): vertices to be removed from the graph.
        """
        [self.remove(v) for v in vertices]

    @dispatch
    def remove(self, vertex=None):
        """
        @overload.

        Removes vertex(s) from the graph.

        Calls:
            1.  remove single vertex from the graph.
                Args:
                    vertex (GraphVertex): a vertex to be removed from the graph.

            2.  remove multiple vertices from the graph.
                Args:
                    vertices (Iterable[GraphVertex]): vertices to be removed from the graph.
        """

    def update_optimizable_vertices(self, new_values: gtsam.Values) -> None:
        """Updates optimizable vertices with new values.

        Args:
            new_values (gtsam.Values).
        """

        [vertex.update(new_values) for vertex in self._optimizable_vertices]

    def update_non_optimizable_vertices(self) -> None:
        """Updates non-optimizable vertices."""
        [vertex.update() for vertex in self._not_optimizable_vertices]

    @staticmethod
    def find_closest_vertex(
        vertex_type: type[GraphVertex], timestamp: int, margin: int
    ) -> GraphVertex | None:
        """Finds the closest vertex with the given timestamp, time margin and type.

        TODO: add implementation.

        algorithm:
            1.  from vertices storage get all ve.
            2.  if not found, find the closest vertex with the given time margin.

        Args:
            vertex_type (type[GraphVertex): type of vertex to find.
            timestamp (int): timestamp to compare with.
            margin (int): margin for the search.

        Returns:
            (GraphVertex | None): closest vertex if found, None otherwise.
        """
        raise NotImplementedError

    def get_last_vertex(self, vertex_type: type[GraphVertex]) -> GraphVertex | None:
        """
        Gets the previous vertex from the graph.
        Args:
            vertex_type (type[GraphVertex]): type of the vertex to find.

        Returns:
            (GraphVertex): previous vertex.
        """
        msg = f"No previous vertex of type {vertex_type.__name__!r} found."
        try:
            v = self.get_vertices(vertex_type)[-1]
            return v
        except IndexError:
            logger.info(msg)
            return None
        except KeyError:
            logger.info(msg)
            return None

    def _add_to_table(self, vertex: GraphVertex) -> None:
        """Adds vertex to the vertices table.

        Args:
            vertex (GraphVertex): vertex to be added to the table.
        """
        t = type(vertex)
        if t not in self._vertices_table:
            raise KeyError(f"Type {t!r} has not been defined in the vertices table.")
        self._vertices_table[t].add(vertex)

    def _remove_from_table(self, vertex: GraphVertex) -> None:
        """Removes vertex from the vertices table.

        Args:
            vertex (GraphVertex): vertex to be removed from the table.
        """
        t = type(vertex)
        if t not in self._vertices_table:
            raise KeyError(f"Type {t!r} has not been defined in the vertices table.")
        self._vertices_table[t].remove(vertex)
