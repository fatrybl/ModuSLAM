"""TODO: add tests"""

import concurrent.futures
from collections.abc import Callable, Iterable
from typing import TypeAlias

import numpy as np
import open3d as o3d
from sklearn.neighbors import NearestNeighbors

from src.custom_types.numpy import Matrix4x4, MatrixNx3
from src.external.metrics.modified_mom.config import BaseConfig, HdbscanConfig
from src.external.metrics.modified_mom.hdbscan_planes import extract_orthogonal_subsets
from src.external.metrics.modified_mom.utils import (
    aggregate_map,
    compute_entropy,
    compute_plane_variance,
    compute_variances,
)
from src.external.metrics.utils import median

Cloud: TypeAlias = o3d.geometry.PointCloud


def mom(
    clouds: list[Cloud],
    ts: list[Matrix4x4],
    mom_config: BaseConfig,
    plane_detection_config: HdbscanConfig,
    subsets: Iterable[MatrixNx3] | None = None,
):
    """Mutually Orthogonal Metric.
    https://www.researchgate.net/publication/352572583_Be_your_own_Benchmark_No-Reference_Trajectory_Metric_on_Registered_Point_Clouds

    Args:
        clouds: 3D point clouds.

        ts: transformation matrices (i.e., Point Cloud poses).

        mom_config: parameters for MOM metric.

        plane_detection_config: parameters for plane detection algorithm.

        subsets: mutually orthogonal subsets.

    Returns:
        MOM value.

    TODO: add tests.
    """
    orth_axes_stats = []

    pc_map = aggregate_map(clouds, ts)
    points = np.asarray(pc_map.points)
    nn_model = NearestNeighbors(radius=mom_config.knn_rad)
    nn_model.fit(points)

    if subsets:
        orth_clouds = subsets
    else:
        pcd = median(clouds)
        orth_clouds = extract_orthogonal_subsets(pcd, mom_config, plane_detection_config)
        # orth_clouds = extract_orthogonal_subsets(pcd, eps=0.5)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                compute_variances,
                cloud,
                points,
                nn_model,
                mom_config.knn_rad,
                mom_config.min_neighbours,
            )
            for cloud in orth_clouds
        ]
        for future in concurrent.futures.as_completed(futures):
            orth_axes_stats.append(future.result())

    return np.sum(orth_axes_stats)


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
    return mean_map_metric(pcs, ts, config, compute_entropy)


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
    return mean_map_metric(pcs, ts, config, compute_plane_variance)


def mean_map_metric(
    pcs: list[Cloud],
    ts: list[Matrix4x4],
    config: BaseConfig,
    alg: Callable,
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
        _, idx, _ = map_tree.search_radius_vector_3d(point, config.knn_rad)
        if len(idx) > config.min_knn:
            metric_value = alg(points[idx])
            if metric_value is not None:
                metric.append(metric_value)

    result = 0.0 if len(metric) == 0 else np.mean(metric)
    return result
