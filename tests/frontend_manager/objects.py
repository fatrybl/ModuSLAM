from typing import Any

import gtsam

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.edge_factories.interface import EdgeFactory
from moduslam.frontend_manager.graph.base_edges import UnaryEdge
from moduslam.frontend_manager.graph.base_vertices import NotOptimizableVertex
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.handlers.interface import Handler
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.ordered_set import OrderedSet


def create_measurement(handler: Handler, element: Element):
    return Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        value=element.measurement.values,
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )


class BasicTestHandler(Handler):

    def __init__(self, cfg: HandlerConfig):
        self._name = cfg.name

    @property
    def name(self) -> str:
        return self._name

    def process(self, element: Element) -> Measurement | None:
        m = create_measurement(self, element)
        return m

    @staticmethod
    def create_empty_element(element: Element) -> Element:
        return element


class BasicTestVertex(NotOptimizableVertex):
    def update(self, value: Any) -> None: ...


class BasicTestEdgeFactory(EdgeFactory):
    def __init__(self, config: EdgeFactoryConfig):
        self._name = config.name

    @property
    def name(self) -> str:
        return self._name

    def create(
        self, graph: Graph, measurements: OrderedSet[Measurement], timestamp: int
    ) -> list[UnaryEdge]:

        m = measurements[0]

        f = gtsam.PriorFactorPoint2(
            key=0, prior=[0, 0], noiseModel=gtsam.noiseModel.Diagonal.Sigmas([1, 1])
        )
        noise = gtsam.noiseModel.Diagonal.Sigmas([1, 1])

        edge = UnaryEdge(vertex=BasicTestVertex(), measurement=m, noise_model=noise, factor=f)
        return [edge]
