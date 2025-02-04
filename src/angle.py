import math

from src.utils.auxiliary_dataclasses import Position2D


def calculate_angle(point1: Position2D, point2: Position2D) -> float:
    """
    Calculate the angle between two 2D points.

    Args:
        point1: 1-st point
        point2: 2-nd point.

    Returns:
        angle in degrees.
    """
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y

    delta_x = x2 - x1
    delta_y = y2 - y1

    angle_radians = math.atan2(delta_y, delta_x)
    return angle_radians


p1 = Position2D(315610.78409584797919, 4155433.4416373516433)
p2 = Position2D(315610.78673472336959, 4155433.4410236971453)
print(calculate_angle(p1, p2))
