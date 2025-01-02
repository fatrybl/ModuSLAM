import concurrent.futures
from collections.abc import Iterable
from typing import Callable, TypeAlias

import numpy as np
import open3d as o3d
from sklearn.neighbors import NearestNeighbors

from phd.modified_mom.config import BaseConfig
from phd.modified_mom.utils import extract_orthogonal_subsets
from phd.moduslam.custom_types.numpy import Matrix4x4, MatrixNx3

Cloud: TypeAlias = o3d.geometry.PointCloud


def _compute_variances(target_points, source_points, nn_model, knn_rad: float, min_neighbours: int):
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

    metrics = np.array([_plane_variance(source_points[idx]) for idx in valid_indices])
    return np.median(metrics)


def mom(
    clouds: list[Cloud],
    ts: list[Matrix4x4],
    config: BaseConfig = BaseConfig(),
    subsets: Iterable[Cloud] | None = None,
):
    """Mutually Orthogonal Metric.
    https://www.researchgate.net/publication/352572583_Be_your_own_Benchmark_No-Reference_Trajectory_Metric_on_Registered_Point_Clouds

    Args:
        clouds: 3D point clouds.

        ts: transformation matrices (i.e., Point Cloud poses).

        config: scene hyperparameters.

        subsets: mutually orthogonal subsets.

    Returns:
        MOM value.
    """
    pc_map = aggregate_map(clouds, ts)
    points = np.asarray(pc_map.points)
    nn_model = NearestNeighbors(radius=config.KNN_RAD)
    nn_model.fit(points)

    if subsets:
        matrices_list: list[MatrixNx3] = [np.asarray(cloud.points) for cloud in subsets]

    else:
        matrices_list, _, _ = extract_orthogonal_subsets(pc_map, config)

    orth_axes_stats = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                _compute_variances, matrix, points, nn_model, config.KNN_RAD, config.MIN_NEIGHBOURS
            )
            for matrix in matrices_list
        ]
        for future in concurrent.futures.as_completed(futures):
            orth_axes_stats.append(future.result())

    return np.sum(orth_axes_stats)


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


def _plane_variance(points: MatrixNx3) -> float:
    """Computes plane variance of given points.

    Args:
        points: array of 3D points.

    Returns:
        points plane variance.
    """
    cov = np.cov(points.T)
    eigenvalues, _ = np.linalg.eigh(cov)
    return np.min(eigenvalues)


def _entropy(points: MatrixNx3) -> float | None:
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


def _mean_map_metric(
    pcs: list[Cloud],
    ts: list[Matrix4x4],
    config: BaseConfig = BaseConfig(),
    alg: Callable = _plane_variance,
) -> float:
    """No-reference metric algorithms' helper.

    Args:
        pcs: point clouds obtained from sensors.

        ts: transformation matrices list (i.e., Point Cloud poses).

        config: scene hyperparameters.

        alg: metric algorithm basis (e.g., plane variance, entropy)

    Returns:
        mean of given metric algorithm values.
    """
    pc_map = aggregate_map(pcs, ts)

    map_tree = o3d.geometry.KDTreeFlann(pc_map)
    points = np.asarray(pc_map.points)
    metric = []
    for i in range(points.shape[0]):
        point = points[i]
        _, idx, _ = map_tree.search_radius_vector_3d(point, config.KNN_RAD)
        if len(idx) > config.MIN_KNN:
            metric_value = alg(points[idx])
            if metric_value is not None:
                metric.append(metric_value)

    return 0.0 if len(metric) == 0 else np.mean(metric)


def mme(pcs: list[Cloud], ts: list[Matrix4x4], config: BaseConfig = BaseConfig()) -> float:
    """Mean Map Entropy.
    A no-reference metric algorithm based on entropy.

    Args:
        pcs: point clouds obtained from sensors.

        ts: transformation matrices list (i.e., Point Cloud poses).

        config: scene hyperparameters.

    Returns:
        mean of given metric algorithm values.
    """
    return _mean_map_metric(pcs, ts, config, alg=_entropy)


def mpv(pcs: list[Cloud], ts: list[Matrix4x4], config: BaseConfig = BaseConfig()) -> float:
    """Mean Plane Variance.
    A no-reference metric algorithm based on plane variance.

    Args:
        pcs: point clouds obtained from sensors.

        ts: transformation matrices list (i.e., Point Cloud poses).

        config: scene hyperparameters

    Returns:
        mean of given metric algorithm values
    """
    return _mean_map_metric(pcs, ts, config, alg=_plane_variance)
