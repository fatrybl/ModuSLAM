import logging
from collections.abc import Iterable
from copy import deepcopy

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.utils import add_elements_to_graph, process_leftovers
from phd.exceptions import SkipItemException
from phd.external.variants_factory import Factory as VariantsFactory
from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import (
    GraphCandidate,
    GraphElement,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)

logger = logging.getLogger(__name__)


class Factory:
    @classmethod
    def create_candidates(cls, graph: Graph, storage: MeasurementStorage) -> list[GraphCandidate]:
        """Creates graph candidates.

        Args:
            graph: a graph to create candidates for.

            storage: a storage with measurements.
        """
        variants = VariantsFactory.create(storage)
        candidates: list[GraphCandidate] = []

        for variant in variants:
            elements: list[GraphElement] = []
            graph_copy = deepcopy(graph)

            measurements_clusters, leftovers = process_leftovers(variant)

            for m_cluster in measurements_clusters:
                cluster = VertexCluster()

                for measurement in m_cluster.measurements:
                    edge_factory = cls._get_factory(measurement)

                    try:
                        item = edge_factory.create(graph_copy, cluster, measurement)
                        add_elements_to_graph(graph_copy, item)
                        cls._expand_elements(elements, item)

                    except SkipItemException:
                        logger.warning(f"Skipping measurement:{measurement}")

            new_candidate = GraphCandidate(graph_copy, elements, leftovers)
            candidates.append(new_candidate)

        return candidates

    @staticmethod
    def _expand_elements(
        elements: list[GraphElement], item: GraphElement | list[GraphElement]
    ) -> None:
        """Expands elements with a new item.

        Args:
            elements: a list to expand.

            item: a new item or a list of new items.
        """
        if isinstance(item, Iterable):
            for element in item:
                elements.append(element)
        else:
            elements.append(item)

    @staticmethod
    def _get_factory(measurement: Measurement) -> EdgeFactory:
        """Gets the edge factory for a given measurement."""
        raise NotImplementedError
