import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import open3d as o3d
from sklearn.neighbors import NearestNeighbors

from phd.moduslam.custom_types.numpy import MatrixNx3


def filter_normals(
    cloud: o3d.geometry.PointCloud, knn_rad: float, eigen_scale: float, min_neighbours: int = 3
) -> tuple[MatrixNx3, MatrixNx3]:
    """Filters normals based on Eigen values of neighbouring point cloud.

    Args:
        cloud: point cloud.

        knn_rad: KNN radius.

        eigen_scale: eigenvalue scale.

        min_neighbours: minimum number of neighbours.

    Returns:
        filtered normals, filtered points.
    """
    new_normals = []
    new_points = []
    points = np.asarray(cloud.points)
    main_normals = np.asarray(cloud.normals)
    num_points = points.shape[0]
    num_cpu_cores: int | None = os.cpu_count()
    num_batches = num_cpu_cores if num_cpu_cores is not None else 1

    batches = create_batches(num_points, num_batches)

    with ProcessPoolExecutor(max_workers=num_batches) as executor:
        futures = [
            executor.submit(
                process_batch, batch, points, main_normals, knn_rad, eigen_scale, min_neighbours
            )
            for batch in batches
        ]

        for future in as_completed(futures):
            normals_batch, points_batch = future.result()
            new_normals.extend(normals_batch)
            new_points.extend(points_batch)

    return np.vstack(new_normals), np.vstack(new_points)


def process_batch(
    batch_indices: range,
    points: MatrixNx3,
    main_normals: MatrixNx3,
    knn_rad: float,
    eigen_scale: float,
    min_neighbours: int,
) -> tuple[list[MatrixNx3], list[MatrixNx3]]:
    """Processes a batch of points.

    Args:
        batch_indices: indices of the batch.

        points: 3D points.

        main_normals: main normals.

        knn_rad: KNN radius.

        eigen_scale: eigenvalue scale.

        min_neighbours: minimum number of neighbours.

    Returns:
        new normals, new points.
    """

    nn_model = NearestNeighbors(radius=knn_rad)
    nn_model.fit(points)
    new_normals = []
    new_points = []

    indices = nn_model.radius_neighbors(points[batch_indices], return_distance=False)

    for i, indices_i in zip(batch_indices, indices):
        neighbours = points[indices_i]
        num_neighbours = neighbours.shape[0]

        if num_neighbours > min_neighbours:
            status = evaluate_cloud(neighbours, eigen_scale)
            if status:
                new_normals.append(main_normals[i])
                new_points.append(points[i])

    return new_normals, new_points


def evaluate_cloud(points: MatrixNx3, eigen_scale: float) -> bool:
    """Evaluates 3D points based on Eigen values.

    Args:
        points: 3D points.

        eigen_scale: eigenvalue scale.

    Returns:
        status.
    """
    covariance = np.cov(points.T)
    eigenvalues, _ = np.linalg.eigh(covariance)
    return eigenvalues[1] > eigen_scale * eigenvalues[0]


def create_batches(num_points: int, num_batches: int) -> list[range]:
    """Creates batches of indices for processing.

    Args:
        num_points: Total number of points.

        num_batches: Number of batches to create.

    Returns:
        list of ranges representing batches.
    """
    batch_size = num_points // num_batches
    batches = [range(i * batch_size, (i + 1) * batch_size) for i in range(num_batches)]
    if num_points % num_batches != 0:
        batches[-1] = range((num_batches - 1) * batch_size, num_points)
    return batches
