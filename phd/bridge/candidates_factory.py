from collections.abc import Iterable
from copy import deepcopy

from phd.bridge.auxiliary_dataclasses import CandidateWithClusters
from phd.bridge.distributor import get_factory
from phd.bridge.utils import add_elements_to_graph, get_clusters_and_leftovers
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


class Factory:
    """Creates all possible graph candidates."""

    @classmethod
    def create_candidates(
        cls, graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> list[CandidateWithClusters]:
        """Creates graph candidates.

        Args:
            graph: a graph to create candidates for.

            data: a table of typed Ordered Sets with measurements.

        Returns:
            graph candidates with clusters of measurements.
        """
        items: list[CandidateWithClusters] = []

        variants = VariantsFactory.create(data)

        for variant in variants:
            graph_copy = deepcopy(graph)

            measurement_clusters, leftovers = get_clusters_and_leftovers(variant)

            elements = cls._create_graph_elements(graph_copy, measurement_clusters)

            graph_candidate = GraphCandidate(graph_copy, elements, leftovers)
            item = CandidateWithClusters(graph_candidate, measurement_clusters)

            items.append(item)

        return items

    @classmethod
    def _create_graph_elements(
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
