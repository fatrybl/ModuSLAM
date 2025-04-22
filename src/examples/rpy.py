import math
from typing import Tuple

from src.utils.auxiliary_objects import zero_vector3


def compute_roll_pitch_yaw(
    point1: Tuple[float, float, float], point2: Tuple[float, float, float]
) -> Tuple[float, float, float]:
    """
    Computes the roll, pitch, and yaw angles between two points in 3D space.

    Args:
        point1: A tuple representing the first point (x1, y1, z1).
        point2: A tuple representing the second point (x2, y2, z2).

    Returns:
        A tuple containing the roll, pitch, and yaw angles in radians.
    """
    # Calculate the direction vector
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]

    # Compute the yaw angle (rotation around the z-axis)
    yaw = math.atan2(dy, dx)

    # Compute the pitch angle (rotation around the y-axis)
    pitch = math.atan2(-dz, math.sqrt(dx**2 + dy**2))

    # Compute the roll angle (rotation around the x-axis)
    roll = 0.0  # Roll is not defined for a direction vector between two points

    return roll, pitch, yaw


if __name__ == "__main__":
    # Example usage
    point1 = zero_vector3
    point2 = (-0.0025537763722240925, 0.00541700329631567, -0.0006000000000057071)
    roll, pitch, yaw = compute_roll_pitch_yaw(point1, point2)
    print(f"Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}")
