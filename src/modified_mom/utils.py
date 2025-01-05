from typing import TypeAlias

import networkx as nx
import numpy as np
import open3d as o3d
from sklearn.cluster import HDBSCAN

from src.modified_mom.config import BaseConfig
from src.modified_mom.normals_filter import filter_normals
from src.moduslam.custom_types.numpy import Matrix4x4, MatrixNx3, Vector3, VectorN

Cloud: TypeAlias = o3d.geometry.PointCloud


def extract_orthogonal_subsets(
    pc: Cloud, config: BaseConfig = BaseConfig()
) -> tuple[list[MatrixNx3], list[MatrixNx3], list[Vector3]]:
    """Extracts point clouds which mean norman vectors are mutually orthogonal.

    Args:
        pc: point cloud.

        config: configuration for the algorithm.

    Returns:
        orthogonal clouds , normals, clique normals.
    """
    pc_cut = estimate_normals(pc, config.KNN_RAD, config.MAX_NN, config.EIGEN_SCALE)
    normals = np.asarray(pc_cut.normals)

    clustering = HDBSCAN(
        min_cluster_size=config.MIN_CLUST_SIZE,
        cluster_selection_epsilon=0.2,
        alpha=1.5,
        n_jobs=-1,
    )

    clustering.fit(normals)
    labels = clustering.labels_

    cluster_means, cluster_means_ind = filter_clusters(
        labels, normals, min_clust_size=config.MIN_CLUST_SIZE
    )

    max_clique = find_max_clique(
        labels, cluster_means, cluster_means_ind, eps=config.ORTHOGONALITY_EPS
    )

    pc_points = np.asarray(pc_cut.points)
    pc_normals = np.asarray(pc_cut.normals)

    masks = [labels == cluster_means_ind[i] for i in max_clique]

    orth_subset = [pc_points[mask] for mask in masks]
    orth_normals = [pc_normals[mask] for mask in masks]
    clique_normals = [cluster_means[i] for i in max_clique]

    return orth_subset, orth_normals, clique_normals


def estimate_normals(pc: Cloud, knn_rad: float, max_nn: int, eigen_scale: float) -> Cloud:
    """Estimates normals for a point cloud.

    Args:
        pc: point cloud.

        knn_rad: k-nearest neighbors radius.

        max_nn: maximum number of neighbors.

        eigen_scale: scale for eigen values.

    Returns:
        point cloud with normals.
    """
    cut_pcd = o3d.geometry.PointCloud()

    if not pc.has_normals():
        param = o3d.geometry.KDTreeSearchParamHybrid(radius=knn_rad, max_nn=max_nn)
        pc.estimate_normals(search_param=param)

    normals, points = filter_normals(pc, knn_rad, eigen_scale)

    cut_pcd.points = o3d.utility.Vector3dVector(points)
    cut_pcd.normals = o3d.utility.Vector3dVector(normals)

    return cut_pcd


def filter_clusters(
    labels: VectorN, normals: MatrixNx3, min_clust_size: int
) -> tuple[MatrixNx3, list[int]]:
    """Filters clusters based on their size.

    Args:
        labels: cluster labels.

        normals: normal vectors.

        min_clust_size: minimum cluster size.

    Returns:
        cluster mean normals, cluster indices
    """
    cluster_means: list[MatrixNx3] = []
    cluster_means_ind = []

    unique_labels, counts = np.unique(labels, return_counts=True)
    large_clusters = unique_labels[counts >= min_clust_size]

    indices = np.isin(labels, large_clusters)
    filtered_normals = normals[indices]
    filtered_labels = labels[indices]

    for cluster_id in large_clusters:
        cluster_indices = filtered_labels == cluster_id
        normals_array = filtered_normals[cluster_indices]
        mean_normals = np.mean(normals_array, axis=0)
        cluster_means.append(mean_normals)
        cluster_means_ind.append(cluster_id)

    means = np.vstack(cluster_means)
    means = means / np.linalg.norm(means, axis=1)[:, None]

    return means, cluster_means_ind


def find_max_clique(
    labels: VectorN, cluster_means: MatrixNx3, cluster_means_ind: list[int], eps: float
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


def read_orthogonal_subset(subset_path: str, pose_path: str, ts: list[Matrix4x4]):
    """Reads and aggregates an orthogonal subset.

    Args:
        subset_path: orthogonal subset data.

        pose_path: pose of orthogonal subset in the map.

        ts: transformation (4x4) matrices list (i.e., Point Cloud poses)

    Returns:
        aggregated orthogonal subset.
    """
    orth_list = np.load(subset_path, allow_pickle=True)
    orth_pose = np.loadtxt(pose_path, usecols=range(4))
    orth_pose = np.linalg.inv(ts[0]) @ orth_pose

    aggregated_subset = []
    for surface in orth_list:
        cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(surface))
        transformed_points = cloud.transform(orth_pose).points
        aggregated_subset.append(transformed_points)

    return aggregated_subset
