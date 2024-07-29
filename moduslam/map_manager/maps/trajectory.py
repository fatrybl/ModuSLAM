"""Trajectory of SE(3) poses with timestamps."""

from moduslam.types.numpy import Matrix4x4


class TrajectoryMap:

    def __init__(self):
        self._items: list[tuple[int, Matrix4x4]] = []

    @property
    def poses(self) -> list[Matrix4x4]:
        """SE(3) poses."""
        poses = [pose for _, pose in self._items]
        return poses

    @property
    def timestamps(self) -> list[int]:
        """Timestamps of poses."""
        timestamps = [t for t, _ in self._items]
        return timestamps

    @property
    def trajectory(self) -> list[tuple[int, Matrix4x4]]:
        """Timestamps with poses."""
        return self._items

    def add(self, timestamp: int, pose: Matrix4x4) -> None:
        """Adds pose with timestamp to the trajectory.

        Args:
            timestamp: timestamp of the pose.

            pose: SE(3) pose.
        """
        self._items.append((timestamp, pose))
