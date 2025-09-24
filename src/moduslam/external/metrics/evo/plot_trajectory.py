from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from evo.core import sync
from evo.core.trajectory import PoseTrajectory3D
from evo.tools import plot
from pyquaternion import Quaternion

from moduslam.map_manager.trajectory import load_trajectory_from_txt
from moduslam.utils.auxiliary_methods import microsec2nanosec, str_to_float


def load_gt_trajectory(file_path: Path) -> list:
    """Loads a trajectory from a .txt file with the format: time(us) px py pz qx qy qz
    qw.

    Args:
        file_path: a Path to the .txt file.

    Returns:
        timestamps with SE(3) poses.
    """
    trajectory = []

    with file_path.open("r") as f:
        next(f)  # Skip header
        for line in f:
            values = line.strip().split()
            timestamp = microsec2nanosec(str_to_float(values[0]))
            px, py, pz = map(str_to_float, values[1:4])
            qx, qy, qz, qw = map(str_to_float, values[4:])

            # Convert quaternion to rotation matrix
            quat = Quaternion(qw, qx, qy, qz)
            rotation_matrix = quat.rotation_matrix

            # Create SE(3) matrix
            matrix = np.eye(4)
            matrix[:3, :3] = rotation_matrix
            matrix[:3, 3] = [px, py, pz]

            trajectory.append((timestamp, matrix))

    return trajectory


def convert_to_evo_trajectory(traj: list) -> PoseTrajectory3D:
    """Converts a trajectory to an EVO PoseTrajectory3D.

    Args:
        traj: timestamps with SE(3) matrices.

    Returns:
        EVO PoseTrajectory3D object.
    """
    poses = []
    ts = []
    for timestamp, pose in traj:
        ts.append(timestamp)
        poses.append(pose)

    ts_array = np.array(ts, dtype=np.float64)
    poses_array = np.stack(poses, axis=0)
    return PoseTrajectory3D(timestamps=ts_array, poses_se3=poses_array)


def load_and_sync_trajectories(
    file1: Path, file2: Path
) -> tuple[PoseTrajectory3D, PoseTrajectory3D]:
    """Loads and synchronizes two trajectories.

    Args:
        file1: a file with reference trajectory.
        file2: a file with estimated trajectory.

    Returns:
        reference & estimated trajectories.
    """
    ref = load_gt_trajectory(file1)
    est = load_trajectory_from_txt(file2)  # Assuming the same format for simplicity

    ref_evo = convert_to_evo_trajectory(ref)
    est_evo = convert_to_evo_trajectory(est)

    time_diff = est_evo.timestamps[-1] - est_evo.timestamps[0]
    ref_evo, est_evo = sync.associate_trajectories(ref_evo, est_evo, max_diff=time_diff)
    return ref_evo, est_evo


def plot_trajectories_3d(ref_traj: PoseTrajectory3D, est_traj: PoseTrajectory3D):
    """Plots both estimated and reference trajectories in 3D using evo tools and adds
    coordinate frames to each pose.

    Args:
        ref_traj: reference trajectory.
        est_traj: estimated trajectory.
    """
    mode = plot.PlotMode.xyz
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    traj_by_label = {
        # "Reference Trajectory": ref_traj,
        "Estimated Trajectory": est_traj,
    }
    # plot.draw_coordinate_axes(ax, ref_traj, plot_mode=mode, marker_scale=0.1)
    plot.draw_coordinate_axes(ax, est_traj, plot_mode=mode, marker_scale=0.2)
    plot.trajectories(ax, traj_by_label, mode, plot_start_end_markers=True, title="Trajectories")
    plt.show()


if __name__ == "__main__":
    # Define file paths
    ref_file = Path("/media/mark/WD/tum/visual_inertial_event/loop_floor_0/mocap_data.txt")
    est_file = Path("/home/mark/Desktop/PhD/ModuSLAM/src/moduslam/trajectory.txt")

    # Load and synchronize trajectories
    ref_traj, est_traj = load_and_sync_trajectories(ref_file, est_file)

    # Plot the trajectories
    plot_trajectories_3d(ref_traj, est_traj)
