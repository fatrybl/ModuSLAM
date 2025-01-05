import random
from pathlib import Path

import numpy as np
import open3d as o3d

from src.external.metrics.modified_mom.config import LidarConfig
from src.external.metrics.modified_mom.hdbscan_planes import extract_orthogonal_subsets
from src.external.metrics.modified_mom.metrics import mom
from src.moduslam.custom_types.numpy import Matrix4x4, MatrixNx3
from src.moduslam.map_manager.utils import read_4_channel_bin_pcd
from src.utils.exceptions import DimensionalityError


def visualize_point_cloud_with_subsets(pcd, planes):
    """
    Visualize the entire point cloud in grey and three subsets of points with RGB colors.

    Parameters:
    - pcd: open3d.geometry.PointCloud object
    - planes: List of numpy arrays [subset1, subset2, subset3, ...]
      Each subset should have shape (N, 3), where N is the number of points in the subset.
    """
    # Visualize the entire point cloud in grey color
    pcd_visual = pcd
    pcd_visual.paint_uniform_color([0.5, 0.5, 0.5])  # Set point cloud to grey color

    # Define initial colors for the subsets (RGB colors for the planes)
    subset_colors = [
        np.array([1, 0, 0]),  # Red for subset 1
        np.array([0, 1, 0]),  # Green for subset 2
        np.array([0, 0, 1]),  # Blue for subset 3
    ]

    # Generate additional colors if there are more than three subsets
    while len(subset_colors) < len(planes):
        subset_colors.append(np.array([random.random(), random.random(), random.random()]))

    # Create point clouds for the subsets
    subset_pcds = []
    for i, plane in enumerate(planes):
        subset = o3d.geometry.PointCloud()
        # Ensure the numpy array is converted to the appropriate Open3D format
        subset.points = o3d.utility.Vector3dVector(plane)
        # Set the color of the subset
        subset.paint_uniform_color(subset_colors[i])
        subset_pcds.append(subset)

    # Combine the original point cloud with the subsets
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # Add the original point cloud (grey) to the visualizer
    vis.add_geometry(pcd_visual)

    # Add each of the subset point clouds (colored)
    for subset in subset_pcds:
        vis.add_geometry(subset)

    # Run the visualization
    vis.run()
    vis.destroy_window()


def visualize_point_cloud_with_subsets_multiple(pcd, planes):
    """
    Visualize the entire point cloud in grey and multiple subsets of points with distinct RGB colors.

    Parameters:
    - pcd: open3d.geometry.PointCloud object
    - planes: List of numpy arrays [subset1, subset2, ...]
      Each subset should have shape (N, 3), where N is the number of points in the subset.
    """
    # Predefined distinct colors
    colors = [
        [1, 0, 0],  # Red
        [0, 1, 0],  # Green
        [0, 0, 1],  # Blue
        [1, 1, 0],  # Yellow
        [0, 1, 1],  # Cyan
        [1, 0, 1],  # Magenta
        [1, 0.5, 0],  # Orange
        [0.5, 0, 0.5],  # Purple
        [0.5, 0.5, 0],  # Olive
        [0, 0.5, 0.5],  # Teal
    ]

    # Visualize the entire point cloud in grey color
    pcd_visual = pcd
    pcd_visual.paint_uniform_color([0.5, 0.5, 0.5])  # Set point cloud to grey color

    # Create point clouds for the subsets
    subset_pcds = []
    for i, plane in enumerate(planes):
        subset = o3d.geometry.PointCloud()
        # Ensure the numpy array is converted to the appropriate Open3D format
        subset.points = o3d.utility.Vector3dVector(plane)
        # Set the color of the subset to a predefined color or a random color if more subsets than colors
        color = (
            colors[i % len(colors)]
            if i < len(colors)
            else [random.random(), random.random(), random.random()]
        )
        subset.paint_uniform_color(color)
        subset_pcds.append(subset)

    # Combine the original point cloud with the subsets
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # Add the original point cloud (grey) to the visualizer
    vis.add_geometry(pcd_visual)

    # Add each of the subset point clouds (colored)
    for subset in subset_pcds:
        vis.add_geometry(subset)

    # Run the visualization
    vis.run()
    vis.destroy_window()


def rotate_pose_around_z(pose: Matrix4x4, angle_degrees: float) -> Matrix4x4:
    """Rotates an SE(3) pose around the z-axis by a given angle.

    Args:
        pose: The original SE(3) pose as a 4x4 numpy array.

        angle_degrees: The angle to rotate around the z-axis in degrees.

    Returns:
        The rotated SE(3) pose as a 4x4 numpy array.
    """
    angle_radians = np.deg2rad(angle_degrees)
    rotation_matrix = np.array(
        [
            [np.cos(angle_radians), -np.sin(angle_radians), 0, 0],
            [np.sin(angle_radians), np.cos(angle_radians), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    rotated_pose = rotation_matrix @ pose
    return rotated_pose


def generate_distinct_colors(num_colors):
    """
    Generate a list of distinct colors.

    Args:
        num_colors: Number of distinct colors to generate.

    Returns:
        List of RGB colors.
    """
    colors = []
    for _ in range(num_colors):
        colors.append([random.random(), random.random(), random.random()])
    return colors


def visualize_point_cloud_with_planes(pcd, planes):
    """
    Visualize the entire point cloud in grey and multiple planes' points with distinct colors.

    Parameters:
    - pcd: open3d.geometry.PointCloud object
    - planes: List of numpy arrays [plane1, plane2, ...]
      Each plane should have shape (N, 3), where N is the number of points in the plane.
    """
    # Visualize the entire point cloud in grey color
    pcd.paint_uniform_color([0.5, 0.5, 0.5])  # Set point cloud to grey color

    # Generate distinct colors for each plane
    colors = generate_distinct_colors(len(planes))

    # Create point clouds for the planes
    plane_pcds = []
    for i, plane in enumerate(planes):
        plane_pcd = o3d.geometry.PointCloud()
        # Ensure the numpy array is converted to the appropriate Open3D format
        plane_pcd.points = o3d.utility.Vector3dVector(plane)
        # Set the color of the plane to a distinct color
        plane_pcd.paint_uniform_color(colors[i])
        plane_pcds.append(plane_pcd)

    # Combine the original point cloud with the planes
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # Add the original point cloud (grey) to the visualizer
    vis.add_geometry(pcd)

    # Add each of the plane point clouds (colored)
    for plane_pcd in plane_pcds:
        vis.add_geometry(plane_pcd)

    # Run the visualization
    vis.run()
    vis.destroy_window()


def array_to_pointcloud(array: MatrixNx3) -> o3d.geometry.PointCloud:
    """
    Convert a numpy array of shape (N, 3) to an Open3D PointCloud.

    Args:
        array: numpy array of shape (N, 3) representing point cloud data.

    Returns:
        Open3D PointCloud object.
    """
    if array.shape[1] != 3:
        raise DimensionalityError("Input array must have shape (N, 3)")

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(array)
    return point_cloud


# Example Usage
if __name__ == "__main__":
    config = LidarConfig()
    config.eigen_scale = 30
    config.min_cluster_size = 10
    config.knn_rad = 1.5
    config.min_knn = 10

    bin_file_path0 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_left/1544581170279399000.bin"
    bin_file_path1 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_right/1544581170243112000.bin"
    bin_file_path2 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_right/1544581170343974000.bin"
    bin_file_path3 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_right/1544581170444842000.bin"
    pcd0 = read_4_channel_bin_pcd(Path(bin_file_path0))
    pcd1 = read_4_channel_bin_pcd(Path(bin_file_path1))
    pcd2 = read_4_channel_bin_pcd(Path(bin_file_path2))
    pcd3 = read_4_channel_bin_pcd(Path(bin_file_path3))

    i4x4 = np.eye(4)

    left_tf_base_sensor = np.asarray(
        [
            [-0.516377, -0.702254, -0.490096, -0.334623],
            [0.491997, -0.711704, 0.501414, 0.431973],
            [-0.700923, 0.0177927, 0.713015, 1.94043],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    right_tf_base_sensor = np.asarray(
        [
            [-0.514521, 0.701075, -0.493723, -0.333596],
            [-0.492472, -0.712956, -0.499164, -0.373928],
            [-0.701954, -0.0136853, 0.712091, 1.94377],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    pcd0.transform(left_tf_base_sensor)
    pcd1.transform(right_tf_base_sensor)
    pcd2.transform(right_tf_base_sensor)
    pcd3.transform(right_tf_base_sensor)
    pcd = pcd1 + pcd2 + pcd3

    subsets, _, _ = extract_orthogonal_subsets(pcd0 + pcd1, config)
    print(f"Num subsets: {len(subsets)}")
    clouds = [array_to_pointcloud(subset) for subset in subsets]

    visualize_point_cloud_with_subsets(pcd1, subsets)

    value = mom([pcd1, pcd2, pcd3], [i4x4, i4x4, i4x4], subsets=clouds, config=config)
    print(f"mom after tf: {value}")

    # tf1 = rotate_pose_around_z(np.eye(4), 5)
    # tf2 = rotate_pose_around_z(np.eye(4), -5)
    tf1 = tf2 = np.eye(4)
    tf1[0, 3] = 0.1
    tf2[0, 3] = 0.1
    pcd = pcd1 + pcd2 + pcd3

    value = mom([pcd1, pcd2, pcd3], [i4x4, tf1, tf2], subsets=clouds, config=config)
    print(f"mom after tf: {value}")
