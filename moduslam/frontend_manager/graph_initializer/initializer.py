import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from moduslam.data_manager.factory.element import Element, RawMeasurement
from moduslam.data_manager.factory.locations import ConfigFileLocation
from moduslam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from moduslam.frontend_manager.graph.custom_vertices import (
    LidarPose,
    LinearVelocity,
    NavState,
    Pose,
)
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.handlers.prior import PriorHandler
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.frontend_manager.graph_initializer.prior import (
    GraphInitializerConfig,
    PriorConfig,
)
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)

FAKE_SENSOR_NAME = "Prior sensor"


class GraphInitializer:
    """Initializes the graph with prior factors."""

    _FAKE_SENSOR_NAME = "Prior sensor"

    def __init__(self, config: GraphInitializerConfig):
        """
        Args:
            config: graph initializer configuration.
        """
        self._sensor = Sensor(SensorConfig(name=self._FAKE_SENSOR_NAME))
        self._handler = PriorHandler()
        self._priors: Iterable[PriorConfig] = config.priors.values()

    def set_prior(self, graph: Graph) -> None:
        """Initializes the graph with prior factors.

        Args:
            graph: a graph to add prior factors in.
        """

        for prior in self._priors:
            edges = self._create_edge(graph, prior)
            graph.add_edges(edges)

    def _create_edge(self, graph: Graph, prior: PriorConfig) -> list[Edge]:
        """Creates an edge with a prior factor.

        Args:
            graph: a graph to add the edge at.

            prior: a prior configuration.

        Returns:
            list with 1 edge.
        """

        measurement = self._init_measurement(
            prior.measurement,
            prior.measurement_noise_covariance,
            prior.timestamp,
            prior.file_path,
        )
        edge_factory = self._get_edge_factory(prior.edge_factory_name)
        edge = edge_factory.create(
            graph=graph,
            measurements=OrderedSet((measurement,)),
            timestamp=prior.timestamp,
        )
        return edge

    @staticmethod
    def _get_new_vertex(graph: Graph, vertex_type: type[Vertex], timestamp: int) -> Vertex:
        """Gets the vertex from the graph by its type and timestamp if exists, otherwise
        creates a new one.

        Args:
            graph (Graph): graph to get vertex from.

            vertex_type (type[Vertex]): vertex type.

            timestamp (int): vertex timestamp.

        Returns:
            vertex.
        """
        vertices = graph.vertex_storage.get_vertices(vertex_type)
        for v in vertices:
            if v.timestamp == timestamp:
                return v

        new_index = generate_index(graph.vertex_storage.index_storage)
        new_vertex = vertex_type(index=new_index, timestamp=timestamp)

        return new_vertex

    @staticmethod
    def _get_edge_factory(factory_name: str) -> EdgeFactory:
        """Gets edge factory with the given name.

        Args:
            factory_name: edge factory name.

        Returns:
            edge factory.
        """
        factory = EdgeFactoriesInitializer.get_factory(factory_name)
        return factory

    def _init_measurement(
        self,
        values: tuple[Any, ...],
        noise_covariance: tuple[float, ...],
        timestamp: int,
        file_path: Path,
    ) -> Measurement:
        """Initializes the measurement.

        Args:
            values: measurement values.

            noise_covariance: covariance of the noise.

            timestamp: timestamp of the measurement.

            file_path: path of the file with the measurement.

        Returns:
            measurement.
        """
        raw_measurement = RawMeasurement(sensor=self._sensor, values=values)

        location = ConfigFileLocation(file_path)

        element = Element(timestamp=timestamp, location=location, measurement=raw_measurement)

        m = Measurement(
            time_range=TimeRange(timestamp, timestamp),
            values=values,
            noise_covariance=noise_covariance,
            handler=self._handler,
            elements=(element,),
        )
        return m

    @staticmethod
    def _get_vertex_type(type_name: str) -> type[Vertex]:
        """Returns the vertex type by its name.

        Args:
            type_name: name of vertex type.

        Returns:
            vertex type.

        Raises:
            ValueError: if the vertex type is not supported.
        """
        match type_name:
            case LidarPose.__name__:
                return LidarPose

            case Pose.__name__:
                return Pose

            case LinearVelocity.__name__:
                return LinearVelocity

            case NavState.__name__:
                return NavState

            case _:
                msg = f"Vertex type {type_name} is not supported."
                logger.critical(msg)
                raise ValueError(msg)
