from collections.abc import Sequence
from dataclasses import dataclass
from typing import TypeAlias

import networkx as nx
import numpy as np
import open3d as o3d
import torch
from torch_ransac3d.plane import plane_fit

from src.moduslam.custom_types.numpy import MatrixNx3

Cloud: TypeAlias = o3d.geometry.PointCloud


@dataclass
class PlaneWithPoints:
    coefficients: tuple[float, float, float, float]
    points: MatrixNx3


def detect_plane(
    cloud: MatrixNx3,
    thresh: float = 0.05,
    max_iterations: int = 1000,
    iterations_per_batch: int = 200,
    epsilon: float = 1e-6,
    device: torch.device = torch.device("cuda"),
) -> tuple[tuple[float, float, float, float], MatrixNx3]:
    """Detects a plane in 3D point cloud using RANSAC.

    Args:
        cloud: a 3D point cloud.

        thresh: a distance threshold for inliers.

        max_iterations: a maximum number of RANSAC iterations.

        iterations_per_batch: a number of iterations per batch.

        epsilon: a convergence tolerance for plane fitting.

        device: a device to run the computations on.

    Returns:
        coefficients of the plane equation ax + by + cz + d = 0, inliers point coordinates.
    """
    tensor = torch.from_numpy(cloud).to(device)

    equation, inliers = plane_fit(
        pts=tensor,
        thresh=thresh,
        max_iterations=max_iterations,
        iterations_per_batch=iterations_per_batch,
        epsilon=epsilon,
        device=device,
    )

    equation = equation.cpu().numpy()
    inlier_points = tensor[inliers].cpu().numpy()

    coefficients = (equation[0], equation[1], equation[2], equation[3])

    return coefficients, inlier_points


def detect_multiple_planes(
    cloud: MatrixNx3,
    thresh: float = 0.02,
    max_iterations: int = 5000,
    iterations_per_batch: int = 1000,
) -> list[PlaneWithPoints]:
    """Detects multiple planes in 3D point cloud using RANSAC.

    Args:
        cloud: a 3D point cloud.

        thresh: a distance threshold for inliers.

        max_iterations: a maximum number of RANSAC iterations.

        iterations_per_batch: a number of iterations per batch.

    Returns:
        list of tuples with coefficients of the plane equation ax + by + cz + d = 0
        and inliers point coordinates.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    result = []

    while cloud.shape[0] >= 3:
        coefficients, inlier_points = detect_plane(
            cloud,
            thresh=thresh,
            max_iterations=max_iterations,
            iterations_per_batch=iterations_per_batch,
            device=device,
        )

        plane_with_points = PlaneWithPoints(coefficients, inlier_points)

        result.append(plane_with_points)

        inlier_indices = np.isin(cloud, inlier_points).all(axis=1)
        cloud = cloud[~inlier_indices]

    return result


def get_max_clique(planes_with_points: Sequence[PlaneWithPoints], eps: float = 1e-1):
    """Finds the maximum clique in the graph of planes.

    Args:
        planes_with_points: list of PlaneWithPoints.

        eps: orthogonality threshold value.

    Returns:
        list of indices of the maximum clique.
    """
    normals = np.array([plane.coefficients[:3] for plane in planes_with_points])
    dot_products = np.abs(np.dot(normals, normals.T))
    adj_matrix = (dot_products < eps).astype(int)
    np.fill_diagonal(adj_matrix, 0)

    D = nx.Graph(adj_matrix)
    cliques = list(nx.algorithms.clique.find_cliques(D))

    cliques = [clique for clique in cliques if len(clique) > 2]
    if not cliques:
        raise ValueError("No cliques of size > 2 found.")

    cliques_sizes = []
    for clique in cliques:
        clique_size = 0

        for i in clique:
            num_points = planes_with_points[i].points.shape[0]
            clique_size += num_points

        cliques_sizes.append(clique_size)

    max_ind = np.argmax(cliques_sizes)
    return cliques[max_ind]


def extract_orthogonal_subsets(pcd: Cloud, eps: float = 1e-1) -> list[MatrixNx3]:
    """Extracts point clouds which mean norman vectors are mutually orthogonal.

    Args:
        pcd: point cloud.

        eps: orthogonality threshold value.

    Returns:
        orthogonal clouds , normals, clique normals.
    """
    points = np.array(pcd.points)
    planes_with_points = detect_multiple_planes(points)

    max_clique = get_max_clique(planes_with_points, eps=eps)

    orth_subset = [planes_with_points[i].points for i in max_clique]

    return orth_subset
