"""TODO: fix __main__ example or remove."""

import math
from collections.abc import Sequence

import matplotlib.pyplot as plt
import networkx as nx

from phd.bridge.auxiliary_dataclasses import ClustersWithConnections, Connection
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.auxiliary import PseudoMeasurement


def visualize_graph_candidates(pairs: Sequence[ClustersWithConnections]) -> None:
    """Visualizes graph candidates on the plot.

    Args:
        pairs: sequence of graph candidates.
    """
    num_candidates = len(pairs)

    num_cols = math.ceil(math.sqrt(num_candidates))
    num_rows = math.ceil(num_candidates / num_cols)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 1 * num_rows))

    # Ensure axes is always iterable
    if num_candidates == 1:
        axes = [axes]  # Wrap single Axes in a list
    else:
        axes = axes.flatten()  # Flatten the axes array for easy indexing

    for i, graph_candidate in enumerate(pairs):
        graph = nx.Graph()

        for vertex in graph_candidate.clusters:
            graph.add_node(vertex)

        for connection in graph_candidate.connections:
            graph.add_edge(connection.cluster1, connection.cluster2)

        # Adjust positions for better fit
        pos = {vertex: (j * 0.8, 0) for j, vertex in enumerate(graph_candidate.clusters)}

        nx.draw_networkx_nodes(
            graph, pos, node_size=400, node_color="lightblue", ax=axes[i]
        )  # Adjust node size

        nx.draw_networkx_edges(
            graph, pos, connectionstyle="arc3,rad=0.2", edge_color="gray", arrows=True, ax=axes[i]
        )

        nx.draw_networkx_labels(
            graph, pos, font_size=7, font_color="black", font_weight="bold", ax=axes[i]
        )

        axes[i].set_title(f"Graph Candidate {i + 1}", fontsize=9)  # Adjust title size

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")
    c1 = MeasurementCluster()
    c2 = MeasurementCluster()
    c3 = MeasurementCluster()

    c1.add(m1)
    c2.add(m2)
    c3.add(m3)

    edge1 = Connection(c1, c2)
    edge2 = Connection(c2, c3)
    edge3 = Connection(c1, c3)

    graph_candidates = [
        ClustersWithConnections(clusters=[c1, c2], connections=[edge1]),
        ClustersWithConnections(clusters=[c2, c3], connections=[edge2]),
        ClustersWithConnections(clusters=[c1, c3], connections=[edge3]),
        ClustersWithConnections(clusters=[c1, c2, c3], connections=[edge1, edge2]),
    ]

    visualize_graph_candidates(graph_candidates)
