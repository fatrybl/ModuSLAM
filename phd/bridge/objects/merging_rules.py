from collections.abc import Callable

from moduslam.frontend_manager.graph.base_vertices import Vertex

rules: dict[type[Vertex], Callable[[list[Vertex]], Vertex]] = {}
