"""TODO: add tests"""

from typing import TypeAlias

import numpy as np
import open3d as o3d

from src.external.metrics.modified_mom.normals_filter import filter_normals
from src.moduslam.custom_types.numpy import Matrix4x4, MatrixNx3, VectorN

Cloud: TypeAlias = o3d.geometry.PointCloud


def aggregate_map(pcs: list[Cloud], ts: list[Matrix4x4]) -> Cloud:
    """Builds a map from point clouds with their poses.

    Args:
        pcs: point clouds obtained from sensors.

        ts: transformation matrices list (i.e., Point Cloud poses).

    Returns:
        pc_map: a map aggregated from point clouds.

    Raises:
        ValueError: the number of point clouds does not match the number of poses.
    """
    if len(pcs) != len(ts):
        raise ValueError("Number of point clouds does not match number of poses")

    pc_map = o3d.geometry.PointCloud()

    first_ts_inv = np.linalg.inv(ts[0])
    new_ts = [first_ts_inv @ T for T in ts]

    for cloud, ts in zip(pcs, new_ts):
        pc_map += cloud.transform(ts)

    return pc_map


def compute_plane_variance(points: MatrixNx3) -> float:
    """Computes plane variance of given points.

    Args:
        points: array of 3D points.

    Returns:
        points plane variance.
    """
    cov = np.cov(points.T)
    eigenvalues, _ = np.linalg.eigh(cov)
    return np.min(eigenvalues)


def compute_entropy(points: MatrixNx3) -> float | None:
    """Computes entropy of given points.

    Args:
        points: array of 3D points.

    Returns:
        points entropy if computed.
    """
    cov = np.cov(points.T)
    det = np.linalg.det(2 * np.pi * np.e * cov)
    if det > 0:
        return 0.5 * np.log(det)

    return None


def compute_variances(target_points, source_points, nn_model, knn_rad: float, min_neighbours: int):
    """Computes plane variances of the clouds made of neighbouring points.

    Args:
        target_points: target points to find neighbours of.

        source_points: all points.

        nn_model: nearest neighbors model.

        knn_rad: k-nearest neighbors radius.

        min_neighbours: minimum number of neighbours per cloud.

    Returns:
        median of plane variances.
    """
    indices = nn_model.radius_neighbors(target_points, radius=knn_rad, return_distance=False)

    valid_indices = [idx for idx in indices if len(idx) > min_neighbours]
    if not valid_indices:
        return np.median([])

    metrics = np.array([compute_plane_variance(source_points[idx]) for idx in valid_indices])
    return np.median(metrics)


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
