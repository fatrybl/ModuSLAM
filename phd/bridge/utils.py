from collections.abc import Iterable

from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.external.objects.auxiliary_classes import SplitPoseOdometry
from phd.external.objects.auxiliary_dataclasses import ClustersWithLeftovers
from phd.external.objects.measurements_cluster import Cluster as MeasurementCluster
from phd.measurements.processed_measurements import Measurement, PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement


def add_elements_to_graph(
    graph: Graph, new_elements: GraphElement | Iterable[GraphElement]
) -> None:
    """Adds new element(s) to the graph.

    Args:
        graph: a graph to which the element(s) will be added.
        new_elements: new element(s) to be added.
    """
    if isinstance(new_elements, Iterable):
        for element in new_elements:
            graph.add_element(element)
    else:
        graph.add_element(new_elements)


def process_leftovers(
    item: list[MeasurementCluster] | ClustersWithLeftovers, leftovers: list[Measurement]
) -> list[MeasurementCluster]:
    """Adds leftovers (if exist) to the database and returns clusters.

    Args:
        item: clusters w or w/o leftovers.

        leftovers: unused measurements.

    Returns:
        clusters.
    """
    if isinstance(item, list):
        return item
    else:
        leftovers.extend(item.leftovers)
        return item.clusters


def solve(graph: Graph) -> float:
    """Solve the problem with the given graph."""
    raise NotImplementedError


def split_odometry(
    measurements: Iterable[PoseOdometry], time_range: TimeRange
) -> list[PoseOdometry | SplitPoseOdometry]:
    """Splits the PoseOdometry measurements into 2 separate measurements if the time
    range is inside the time limits.

    Args:
        measurements: pose odometry measurements.

        time_range: time range within which to split the measurements.

    Returns:
        sorted list of measurements.
    """
    measurements_set: set[PoseOdometry | SplitPoseOdometry] = set(measurements)

    for m in measurements:
        if m.time_range.start >= time_range.start and m.time_range.stop <= time_range.stop:
            split = SplitPoseOdometry(m.timestamp, m)
            measurements_set.remove(m)
            measurements_set.add(split)

    sorted_list = sorted(list(measurements_set), key=lambda x: x.timestamp)
    return sorted_list
