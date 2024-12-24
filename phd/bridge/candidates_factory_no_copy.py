import logging
from collections.abc import Iterable

from phd.bridge.distributor import get_factory
from phd.bridge.utils import add_elements_to_graph, process_leftovers
from phd.external.metrics.factory import MetricsFactory
from phd.external.variants_factory import Factory as VariantsFactory
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphCandidate,
    GraphElement,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.utils.auxiliary_dataclasses import TimeRange
from phd.utils.exceptions import SkipItemException
from phd.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class Factory:
    def __init__(self):
        self._metrics_factory = MetricsFactory()

    def create_candidates(
        self, graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> list[GraphCandidate]:
        """Creates graph candidates.

        Args:
            graph: a graph to create candidates for.

            data: a table of typed Ordered Sets with measurements.
        """
        candidates: list[GraphCandidate] = []
        variants = VariantsFactory.create(data)

        for variant in variants:

            measurement_clusters, leftovers = process_leftovers(variant)

            if len(graph.vertex_storage.clusters) > len(graph.vertex_storage.vertices):
                raise ValueError("Storage is not up-to-date with current clusters.")

            elements = self._process_variant(graph, measurement_clusters)

            candidate = GraphCandidate(graph, elements, leftovers)

            self._metrics_factory.evaluate(candidate, measurement_clusters)

            for element in elements:
                graph.remove_edge(element.edge)

            candidates.append(candidate)

        return candidates

    @staticmethod
    def _process_variant(graph: Graph, clusters: list[MeasurementCluster]) -> list[GraphElement]:
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
                Factory._expand_elements(elements, item)

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
