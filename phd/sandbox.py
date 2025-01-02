import random
from pathlib import Path

import numpy as np
import open3d as o3d

from phd.modified_mom.config import LidarConfig
from phd.modified_mom.metrics import mom
from phd.moduslam.custom_types.numpy import Matrix4x4
from phd.moduslam.map_manager.utils import read_4_channel_bin_pcd


def visualize_point_cloud_with_subsets(pcd, planes):
    """
    Visualize the entire point cloud in grey and three subsets of points with RGB colors.

    Parameters:
    - pcd: open3d.geometry.PointCloud object
    - planes: List of numpy arrays [subset1, subset2, subset3]
      Each subset should have shape (N, 3), where N is the number of points in the subset.
    """
    # Visualize the entire point cloud in grey color
    pcd_visual = pcd
    pcd_visual.paint_uniform_color([0.5, 0.5, 0.5])  # Set point cloud to grey color

    # Define colors for the subsets (RGB colors for the planes)
    subset_colors = [
        np.array([1, 0, 0]),  # Red for subset 1
        np.array([0, 1, 0]),  # Green for subset 2
        np.array([0, 0, 1]),  # Blue for subset 3
    ]

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


# Example Usage
if __name__ == "__main__":
    config = LidarConfig()
    config.EIGEN_SCALE = 10
    config.MIN_CLUST_SIZE = 5
    config.KNN_RAD = 1.5

    bin_file_path1 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_right/1544581170343974000.bin"
    # bin_file_path2 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_left/1544581170279399000.bin"
    pcd1 = read_4_channel_bin_pcd(Path(bin_file_path1))
    # pcd2 = read_4_channel_bin_pcd(Path(bin_file_path2))

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
    pcd1.transform(right_tf_base_sensor)
    # pcd2.transform(left_tf_base_sensor)
    pcd = pcd1

    # o3d.visualization.draw_geometries([pcd])

    # subsets, _, _ = extract_orthogonal_subsets(pcd, config)

    value = mom([pcd], [np.eye(4)], config=config)
    print(f"mom before tf: {value}")

    # tf = np.eye(4)
    # tf = rotate_pose_around_z(tf, -5)
    # pcd2.transform(tf)
    # pcd = pcd1 + pcd2

    # o3d.visualization.draw_geometries([pcd])
    #
    # value = mom([pcd], [np.eye(4)], config=config)
    # print(f"mom after tf: {value}")

    # times = []

    # for _ in range(20):
    #     start_time = time.time()
    #     old_mom([pcd], [np.eye(4)], config=old_cfg)
    #     end_time = time.time()
    #     times.append(end_time - start_time)

    # for _ in range(20):
    #     start_time = time.time()
    #     mom([pcd], [np.eye(4)], config=config)
    #     end_time = time.time()
    #     times.append(end_time - start_time)
    #
    # times = np.array(times)
    # print(f"Execution times: {times}")
    # print(f"Mean execution time: {np.mean(times)} seconds")
    # print(f"Median execution time: {np.median(times)} seconds")
    # print(f"Standard deviation of execution times: {np.std(times)} seconds")
    # print(f"Minimum execution time: {np.min(times)} seconds")
    # print(f"Maximum execution time: {np.max(times)} seconds")

    # print(f"MoM: {mom}")

    # print(mom([pcd1], [np.eye(4)], config=config))

    # visualize_point_cloud_with_subsets(pcd, subsets)
