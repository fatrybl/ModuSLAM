from copy import deepcopy

from src.bridge.auxiliary_dataclasses import CandidateWithClusters
from src.bridge.distributor import get_factory
from src.bridge.utils import add_elements_to_graph, expand_elements
from src.external.variants_factory import Factory as VariantsFactory
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.base import Measurement
from src.moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphCandidate,
    GraphElement,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.exceptions import SkipItemException
from src.utils.ordered_set import OrderedSet


def create_graph_elements(graph: Graph, clusters: list[MeasurementCluster]) -> list[GraphElement]:
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
            expand_elements(elements, item)

    return elements


def create_candidates_with_clusters(
    graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
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

        elements = create_graph_elements(graph_copy, variant.clusters)

        graph_candidate = GraphCandidate(graph_copy, elements, variant.leftovers)
        items.append(CandidateWithClusters(graph_candidate, variant.clusters))

    return items
