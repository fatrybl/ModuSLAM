import logging
from collections.abc import Iterable
from copy import deepcopy

from phd.bridge.distributor import get_factory
from phd.bridge.utils import add_elements_to_graph, process_leftovers
from phd.external.variants_factory import Factory as VariantsFactory
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.storage import MeasurementStorage
from phd.moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphCandidate,
    GraphElement,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import SkipItemException

logger = logging.getLogger(__name__)


class Factory:
    @classmethod
    def create_candidates(cls, graph: Graph, storage: MeasurementStorage) -> list[GraphCandidate]:
        """Creates graph candidates.

        Args:
            graph: a graph to create candidates for.

            storage: a storage with measurements.
        """
        candidates: list[GraphCandidate] = []

        variants = VariantsFactory.create(storage)

        for variant in variants:
            graph_copy = deepcopy(graph)

            measurements_clusters, leftovers = process_leftovers(variant)

            elements = cls._process_variant(graph_copy, measurements_clusters)

            candidates.append(GraphCandidate(graph_copy, elements, leftovers))

        return candidates

    @classmethod
    def _process_variant(
        cls, graph: Graph, clusters: list[MeasurementCluster]
    ) -> list[GraphElement]:
        """Creates graph elements for the given graph and list of clusters with
        measurements.

        Args:
            graph: a graph to create elements for.

            clusters: list of clusters with measurements.

        Returns:
            graph elements.
        """
        elements: list[GraphElement] = []
        local_db: dict[VertexCluster, TimeRange] = {}

        for m_cluster in clusters:
            v_cluster = VertexCluster()
            local_db.update({v_cluster: m_cluster.time_range})

            for measurement in m_cluster.measurements:
                edge_factory = get_factory(type(measurement))

                try:
                    item = edge_factory.create(graph, local_db, measurement)
                except SkipItemException:
                    logger.debug(f"Skipping measurement:{measurement}")
                    continue

                add_elements_to_graph(graph, item)
                cls._expand_elements(elements, item)

        return elements

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
