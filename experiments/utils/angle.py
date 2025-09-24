import csv
from math import atan2

import laspy
import numpy as np
import open3d as o3d

from moduslam.utils.auxiliary_dataclasses import Position2D


def visualize_las_file(file_path: str) -> None:
    """Reads point cloud data from a .las file and visualize it using open3d.

    Args:
        file_path: Path to the .las file.
    """
    las_file = laspy.read(file_path)

    points = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    o3d.visualization.draw_geometries([point_cloud])


def calculate_angle(v1: Position2D, v2: Position2D) -> float:
    """Calculates the angle between two 2D vectors.

    Args:
        v1: 1-st 2D vector.
        v2: 2-nd 2D vector.

    Returns:
        angle in radians.
    """
    x1, y1 = v1.x, v1.y
    x2, y2 = v2.x, v2.y

    delta_x = x2 - x1
    delta_y = y2 - y1

    angle_radians = atan2(delta_y, delta_x)
    return angle_radians


def visualize_trajectory_with_frames(file_path: str) -> None:
    """Reads SE(3) poses from a CSV file and visualizes the trajectory with coordinate
    frames using open3d.

    Args:
        file_path: Path to the CSV file.
    """
    trajectory = []
    frames = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i % 10 == 0:  # Visualize every 10th pose
                pose = np.array(
                    [
                        [float(row[1]), float(row[2]), float(row[3]), float(row[4])],
                        [float(row[5]), float(row[6]), float(row[7]), float(row[8])],
                        [float(row[9]), float(row[10]), float(row[11]), float(row[12])],
                        [0, 0, 0, 1],
                    ]
                )
                trajectory.append(pose[:3, 3])
                frames.append(pose)

    points = np.array(trajectory)
    lines = [[i, i + 1] for i in range(len(points) - 1)]
    colors = [[1, 0, 0] for _ in range(len(lines))]  # Red color for the trajectory lines

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)

    coordinate_frames = []
    for frame in frames:
        coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
        coordinate_frame.transform(frame)
        coordinate_frames.append(coordinate_frame)

    o3d.visualization.draw_geometries([line_set] + coordinate_frames)


p2 = Position2D(332415.06980044580996, 4140883.4476946620271)
p1 = Position2D(332414.69802094681654, 4140884.5215138434432)
print(calculate_angle(p1, p2))


# visualize_las_file("/media/mark/WD/kaist/urban-33/sick_pointcloud.las")
# visualize_trajectory_with_frames("/media/mark/WD/kaist/urban-33/global_pose.csv")
