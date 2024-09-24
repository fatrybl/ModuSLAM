import math

import matplotlib.pyplot as plt
import networkx as nx


def visualize_graph_candidates(graph_candidates):
    num_candidates = len(graph_candidates)

    num_cols = math.ceil(math.sqrt(num_candidates))
    num_rows = math.ceil(num_candidates / num_cols)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 1 * num_rows))

    # Ensure axes is always iterable
    if num_candidates == 1:
        axes = [axes]  # Wrap single Axes in a list
    else:
        axes = axes.flatten()  # Flatten the axes array for easy indexing

    for i, graph_candidate in enumerate(graph_candidates):
        G = nx.Graph()

        for vertex in graph_candidate.vertices:
            G.add_node(vertex)

        for edge in graph_candidate.edges:
            G.add_edge(edge.vertex1, edge.vertex2)

        # Adjust positions for better fit
        pos = {vertex: (j * 0.8, 0) for j, vertex in enumerate(graph_candidate.vertices)}

        nx.draw_networkx_nodes(
            G, pos, node_size=400, node_color="lightblue", ax=axes[i]
        )  # Adjust node size

        nx.draw_networkx_edges(
            G, pos, connectionstyle="arc3,rad=0.2", edge_color="gray", arrows=True, ax=axes[i]
        )

        nx.draw_networkx_labels(
            G,
            pos,
            font_size=7,
            font_color="black",
            font_weight="bold",
            ax=axes[i],  # Adjust font size
        )

        axes[i].set_title(f"Graph Candidate {i + 1}", fontsize=9)  # Adjust title size

    plt.tight_layout()
    plt.show()


# # Example usage
# vertex1 = Vertex((1, 2))
# vertex2 = Vertex((3, 4))
# vertex3 = Vertex((5, 6))
# edge1 = Edge(vertex1, vertex2)
# edge2 = Edge(vertex2, vertex3)
#
# # Create multiple graph candidates for testing
# graph_candidates = [
#     GraphCandidate(vertices=[vertex1, vertex2], edges=[edge1]),
#     GraphCandidate(vertices=[vertex2, vertex3], edges=[edge2]),
#     GraphCandidate(vertices=[vertex1, vertex3], edges=[Edge(vertex1, vertex3)]),
#     GraphCandidate(vertices=[vertex1, vertex2, vertex3], edges=[edge1, edge2]),
# ]
#
# visualize_graph_candidates(graph_candidates)
