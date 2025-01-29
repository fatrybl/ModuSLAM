from typing import TypeAlias

import networkx as nx
import numpy as np
import open3d as o3d
from sklearn.cluster import HDBSCAN

from src.custom_types.numpy import MatrixNx3, VectorN
from src.external.metrics.modified_mom.config import BaseConfig, HdbscanConfig
from src.external.metrics.modified_mom.utils import (
    compute_mean_normals,
    estimate_normals,
)

Cloud: TypeAlias = o3d.geometry.PointCloud


def extract_orthogonal_subsets(
    pc: Cloud, normals_config: BaseConfig, cluster_config: HdbscanConfig
) -> list[MatrixNx3]:
    """Extracts point clouds which mean norman vectors are mutually orthogonal.

    Args:
        pc: a point cloud.

        normals_config: a configuration for normals estimation algorithm.

        cluster_config: a configuration for clustering algorithm

    Returns:
        arrays with orthogonal point clouds.
    """
    pc_cut = estimate_normals(
        pc, normals_config.knn_rad, normals_config.max_nn, normals_config.eigen_scale
    )
    normals = np.asarray(pc_cut.normals)

    clustering = HDBSCAN(
        min_cluster_size=cluster_config.min_cluster_size,
        cluster_selection_epsilon=cluster_config.cluster_selection_epsilon,
        alpha=cluster_config.alpha,
        n_jobs=cluster_config.n_jobs,
        algorithm="brute",
        cluster_selection_method="leaf",
    )

    clustering.fit(normals)
    labels = clustering.labels_

    cluster_means, cluster_means_ind = compute_mean_normals(labels, normals)

    max_clique = find_max_clique(
        labels, cluster_means, cluster_means_ind, eps=normals_config.orthogonality_trh
    )

    pc_points = np.asarray(pc_cut.points)
    # pc_normals = np.asarray(pc_cut.normals)

    masks = [labels == cluster_means_ind[i] for i in max_clique]

    orth_subset = [pc_points[mask] for mask in masks]
    # orth_normals = [pc_normals[mask] for mask in masks]
    # clique_normals = [cluster_means[i] for i in max_clique]

    return orth_subset


def find_max_clique(
    labels: VectorN, cluster_means: MatrixNx3, cluster_means_ind: list[int], eps: float = 1e-1
) -> list[int]:
    """Finds the maximum clique in the graph of cluster mean normals.

    Args:
        labels: cluster labels.

        cluster_means: cluster mean normals.

        cluster_means_ind: cluster mean indices.

        eps: epsilon value.

    Returns:
        maximum clique.
    """
    dot_products = np.abs(np.dot(cluster_means, cluster_means.T))
    adj_matrix = (dot_products < eps).astype(int)
    np.fill_diagonal(adj_matrix, 0)

    D = nx.Graph(adj_matrix)
    cliques = list(nx.algorithms.clique.find_cliques(D))

    cliques = [clique for clique in cliques if len(clique) > 2]
    if not cliques:
        raise ValueError("No cliques of size > 2 found.")

    cliques_sizes = []
    for clique in cliques:
        clique_size = sum(np.sum(labels == cluster_means_ind[j]) for j in clique)
        cliques_sizes.append(clique_size)

    max_ind = np.argmax(cliques_sizes)
    return cliques[max_ind]
