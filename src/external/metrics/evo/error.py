"""Computes the Relative Pose Error (RPE) between two trajectories using EVO package."""

import csv
from pathlib import Path

import numpy as np
from evo.core import metrics, sync
from evo.core.trajectory import PoseTrajectory3D
from evo.tools import plot
from matplotlib import pyplot as plt

from src.custom_types.aliases import Matrix4x4
from src.moduslam.map_manager.trajectory import Trajectory, load_trajectory_from_txt
from src.utils.auxiliary_methods import str_to_float, str_to_int


def sync_trajectories(traj1: PoseTrajectory3D, traj2: PoseTrajectory3D, max_time_diff: float):
    """Synchronizes two trajectories based on their timestamps.

    Args:
        traj1: 1-st trajectory.

        traj2: 2-nd trajectory.

        max_time_diff: the maximum difference between timestamps (time length of trajectory).

    Returns:
        synchronized trajectories.
    """
    traj_ref, traj_est = sync.associate_trajectories(traj1, traj2, max_diff=max_time_diff)
    return traj_ref, traj_est


def load_kaist_gt_trajectory(file_path: Path) -> Trajectory:
    """Loads a trajectory from a .csv file of the Kaist Urban dataset.

    Args:
        file_path: a Path to the .csv file.

    Returns:
        timestamps with SE(3) poses.
    """
    trajectory = []

    with file_path.open("r") as f:
        reader = csv.reader(f)
        for row in reader:
            timestamp = str_to_int(row[0])
            values = list(map(str_to_float, row[1:]))

            matrix = (
                (values[0], values[1], values[2], values[3]),
                (values[4], values[5], values[6], values[7]),
                (values[8], values[9], values[10], values[11]),
                (0.0, 0.0, 0.0, 1.0),
            )
            trajectory.append((timestamp, matrix))

    return trajectory


def convert_to_evo_trajectory(traj: Trajectory) -> PoseTrajectory3D:
    """Converts a trajectory to an EVO PoseTrajectory3D.

    Args:
        traj: timestamps with SE(3) matrices.

    Returns:
        EVO PoseTrajectory3D object.
    """
    poses: list[Matrix4x4] = []
    ts: list[int] = []
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
        file1: a file with reference Kaist Urban trajectory.

        file2: a file with estimated trajectory.

    Returns:
        reference & estimated trajectories.
    """
    ref = load_kaist_gt_trajectory(file1)
    est = load_trajectory_from_txt(file2)

    ref_evo = convert_to_evo_trajectory(ref)
    est_evo = convert_to_evo_trajectory(est)

    time_diff = est_evo.timestamps[-1] - est_evo.timestamps[0]
    ref_evo, est_evo = sync_trajectories(ref_evo, est_evo, time_diff)
    return ref_evo, est_evo


def get_rpe(
    ref: PoseTrajectory3D, est: PoseTrajectory3D, component: metrics.PoseRelation
) -> dict[str, float]:
    """Computes Relative Pose Error.

    Args:
        ref: reference trajectory

        est: estimated trajectory

        component: component of RPE.

    Returns:
        statistics.
    """
    rpe_metric = metrics.RPE(pose_relation=component, all_pairs=True)
    rpe_metric.process_data((ref, est))
    stats = rpe_metric.get_all_statistics()
    return stats


def get_ape(
    ref: PoseTrajectory3D, est: PoseTrajectory3D, component: metrics.PoseRelation
) -> dict[str, float]:
    """Computes Absolute Pose Error.

    Args:
        ref: reference trajectory

        est: estimated trajectory

        component: component of APE.

    Returns:
        statistics.
    """
    ape_metric = metrics.APE(pose_relation=component)
    ape_metric.process_data((ref, est))
    stats = ape_metric.get_all_statistics()
    return stats


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
        "Reference Trajectory": ref_traj,
        "Estimated Trajectory": est_traj,
    }
    plot.draw_coordinate_axes(ax, ref_traj, plot_mode=mode, marker_scale=0.1)
    plot.draw_coordinate_axes(ax, est_traj, plot_mode=mode, marker_scale=0.1)
    plot.trajectories(ax, traj_by_label, mode, plot_start_end_markers=True, title="Trajectories")

    plt.show()


if __name__ == "__main__":
    """Example usage.

    Reference trajectory from the KAIST Urban dataset. Estimated trajectory from
    ModuSLAM. The estimated trajectory is in the form of a .txt file
    """
    ref_file = Path("/media/mark/WD/kaist/urban-26/global_pose.csv")

    traj_dir = Path("/home/mark/Desktop/PhD/ModuSLAM/src/moduslam/")
    est_file = traj_dir / "trajectory.txt"

    ref_traj, est_traj = load_and_sync_trajectories(ref_file, est_file)

    ref_traj.align_origin(est_traj)

    print(len(ref_traj.poses_se3), len(est_traj.poses_se3))

    relation = metrics.PoseRelation.rotation_angle_deg
    rpe_stats = get_rpe(ref_traj, est_traj, relation)
    ape_stats = get_ape(ref_traj, est_traj, relation)

    for metric, value in rpe_stats.items():
        print(metric, value)

    plot_trajectories_3d(ref_traj, est_traj)
