from copy import deepcopy
from typing import cast

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
from src.utils.exceptions import SkipItemException, ValidationError
from src.utils.ordered_set import OrderedSet


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

    for variant in variants:
        graph_copy = deepcopy(graph)

        elements = create_graph_elements(graph_copy, variant.clusters)

        leftovers = cast(list[Measurement], variant.leftovers)
        candidate = GraphCandidate(graph_copy, elements, variant.num_unused_measurements, leftovers)
        items.append(CandidateWithClusters(candidate, variant.clusters))

    return items
