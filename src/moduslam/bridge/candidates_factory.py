from copy import deepcopy
from typing import cast

from moduslam.bridge.auxiliary_dataclasses import (
    CandidateWithClusters,
    ClustersWithLeftovers,
)
from moduslam.bridge.distributor import get_factory
from moduslam.bridge.utils import add_elements_to_graph, expand_elements
from moduslam.external.variants_factory import Factory as VariantsFactory
from moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphCandidate,
    GraphElement,
)
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.base import Measurement
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.exceptions import SkipItemException, ValidationError
from moduslam.utils.ordered_set import OrderedSet


def create_graph_elements(graph: Graph, clusters: list[MeasurementCluster]) -> list[GraphElement]:
    """Creates graph elements for the given graph and list of clusters with
    measurements.

    Args:
        graph: a graph to create elements for.

        clusters: list of clusters with measurements.

    Returns:
        graph elements.

    Raises:
        ValidationError: if any cluster has no core measurements.
    """
    elements: list[GraphElement] = []
    local_db: dict[VertexCluster, TimeRange] = {}

    for m_cluster in clusters:
        v_cluster = VertexCluster()

        try:
            t_range = m_cluster.time_range
        except ValueError:
            raise ValidationError("Measurement cluster must have at least 1 core measurement")

        local_db.update({v_cluster: t_range})

        for measurement in m_cluster.measurements:
            edge_factory = get_factory(type(measurement))

            try:
                item = edge_factory.create(graph, local_db, measurement)
            except SkipItemException:
                continue

            add_elements_to_graph(graph, item)
            expand_elements(elements, item)

    return elements


def process_variant(graph: Graph, variant: ClustersWithLeftovers) -> CandidateWithClusters:
    """Processes a variant of clusters with leftovers and creates a new candidate with
    measurement clusters.

    Args:
        graph: a main graph.

        variant: measurement clusters with leftover measurements.

    Returns:
        a graph candidate with used clusters of measurements.
    """
    elements = create_graph_elements(graph, variant.clusters)
    leftovers = cast(list[Measurement], variant.leftovers)
    candidate = GraphCandidate(graph, elements, variant.num_unused_measurements, leftovers)
    return CandidateWithClusters(candidate, variant.clusters)


# def create_candidates_with_clusters(
#     graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
# ) -> list[CandidateWithClusters]:
#     """Creates graph candidates.
#
#     Args:
#         graph: a graph to create candidates for.
#
#         data: a table of typed Ordered Sets with measurements.
#
#     Returns:
#         graph candidates with clusters of measurements.
#     """
#     items: list[CandidateWithClusters] = []
#
#     if graph.vertex_storage.clusters:
#         latest_cluster = graph.vertex_storage.sorted_clusters[-1]
#         latest_t = latest_cluster.time_range.stop
#     else:
#         latest_t = None
#
#     variants = VariantsFactory.create(data, latest_t)
#     copies = [deepcopy(graph) for _ in variants]
#
#     with ThreadPoolExecutor() as executor:
#         futures = [
#             executor.submit(process_variant, graph, variant)
#             for graph, variant in zip(copies, variants)
#         ]
#         for future in as_completed(futures):
#             items.append(future.result())
#
#     return items


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

    if graph.vertex_storage.clusters:
        latest_cluster = graph.vertex_storage.sorted_clusters[-1]
        latest_t = latest_cluster.time_range.stop
    else:
        latest_t = None

    variants = VariantsFactory.create(data, latest_t)
    copies = [deepcopy(graph) for _ in variants]

    for graph_copy, variant in zip(copies, variants):
        can_with_clusters = process_variant(graph_copy, variant)
        items.append(can_with_clusters)

    return items
