"""Functions to create, save and load a trajectory from a .txt file."""

from collections.abc import Iterable
from pathlib import Path

from src.custom_types.aliases import Matrix4x4
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.auxiliary_methods import str_to_float, str_to_int

Trajectory = list[tuple[int, Matrix4x4]]


def get_trajectory(clusters: Iterable[VertexCluster]) -> Trajectory:
    """Gets a trajectory from the vertex storage.

    Args:
        clusters: clusters with vertices.

    Returns:
        timestamps with SE(3) poses.
    """
    trajectory: Trajectory = []

    for cluster in clusters:
        poses = cluster.get_vertices_of_type(Pose)

        for pose in poses:
            timestamps = cluster.get_timestamps(pose)

            for t in timestamps:
                trajectory.append((t, pose.value))

    return trajectory


def save_trajectory_to_txt(file_path: Path, trajectory: Trajectory) -> None:
    """Saves a trajectory to a .txt file with comma as delimiter using NumPy.

    Args:
        file_path: a Path to the .txt file.
        trajectory: a trajectory to be saved in the file.
    """
    with file_path.open("w") as f:
        for timestamp, matrix in trajectory:
            row_data = ",".join(",".join(map(str, row)) for row in matrix)
            f.write(f"{timestamp},{row_data}\n")


def load_trajectory_from_txt(file_path: Path) -> Trajectory:
    """Loads a trajectory from a .txt file with comma as delimiter.

    Args:
        file_path: a Path to the .txt file.

    Returns:
        timestamps with SE(3) poses.
    """

    trajectory = []
    with file_path.open("r") as f:
        for line in f:
            data = line.strip().split(",")
            timestamp = str_to_int(data[0])
            values = list(map(str_to_float, data[1:]))

            matrix = (
                (values[0], values[1], values[2], values[3]),
                (values[4], values[5], values[6], values[7]),
                (values[8], values[9], values[10], values[11]),
                (values[12], values[13], values[14], values[15]),
            )
            trajectory.append((timestamp, matrix))

    return trajectory
