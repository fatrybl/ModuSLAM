import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from slam.data_manager.factory.element import Element, RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import ConfigFileLocation
from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import Edge
from slam.frontend_manager.graph.base_vertices import Vertex
from slam.frontend_manager.graph.custom_vertices import (
    LidarPose,
    NavState,
    Pose,
    Velocity,
)
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.handlers.prior import PriorHandler
from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.frontend_manager.graph_initializer.prior import (
    GraphInitializerConfig,
    PriorConfig,
)
from slam.system_configs.system.setup_manager.sensors import SensorConfig
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class GraphInitializer:
    """Initializes the graph with prior factors."""

    def __init__(self, config: GraphInitializerConfig):
        self._sensor = Sensor(SensorConfig(name="Prior"))
        self._handler = PriorHandler()
        self._priors: Iterable[PriorConfig] = config.priors.values()

    def set_prior(self, graph: Graph) -> None:
        """Initializes the graph with prior factors.

        Args:
            graph (Graph): graph to add priors at.
        """
        edges: list[Edge] = []

        for prior in self._priors:
            edge = self._create_edge(graph, prior)
            edges.extend(edge)

        graph.add_edge(edges)

    def _create_edge(self, graph: Graph, prior: PriorConfig) -> list[Edge]:
        """Creates an edge with a prior factor.

        Args:
            graph (Graph): graph to add the edge at.
            prior (PriorConfig): prior configuration.

        Returns:
            edge (Edge).
        """
        vertex_type = self._get_vertex_type(prior.vertex_type)
        vertex = vertex_type()

        measurement = self._init_measurement(
            prior.measurement,
            prior.measurement_noise_covariance,
            prior.timestamp,
            prior.file_path,
        )
        edge_factory = self._get_edge_factory(prior.edge_factory_name)
        edge = edge_factory.create(
            graph=graph,
            vertices=(vertex,),
            measurements=OrderedSet((measurement,)),
        )
        return edge

    @staticmethod
    def _get_vertex_type(type_name: str) -> type[Vertex]:
        """
        Returns the vertex type by its name.
        Args:
            type_name (str): vertex type name.

        Returns:
            vertex type (type[Vertex]).
        """
        match type_name:
            case LidarPose.__name__:
                return LidarPose

            case Pose.__name__:
                return Pose

            case Velocity.__name__:
                return Velocity

            case NavState.__name__:
                return NavState

            case _:
                msg = f"Vertex type {type_name} is not supported."
                logger.critical(msg)
                raise ValueError(msg)

    @staticmethod
    def _get_edge_factory(factory_name: str) -> EdgeFactory:
        """Returns the edge factory by its name.

        Args:
            factory_name (str): edge factory name.

        Returns:
            edge factory (EdgeFactory).
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
        """
        Initializes the measurement.
        Args:
            values (tuple[Any, ...]): measurement values.
            noise_covariance (tuple[float, ...]): noise covariance.
            timestamp (int): timestamp of the measurement.
            file_path (Path): file path of the measurement.

        Returns:
            measurement (Measurement).
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
