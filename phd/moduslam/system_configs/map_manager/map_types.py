from dataclasses import dataclass


@dataclass(frozen=True)
class MapType:
    lidar_pointcloud: str = "lidar_pointcloud"
    camera_pointcloud: str = "camera_pointcloud"
    trajectory: str = "trajectory"
