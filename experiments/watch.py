from pathlib import Path

import open3d as o3d

current_dir = Path(__file__).parent.absolute()
sub_dir = "2_lidars_vrs_imu"

current_dir = current_dir / sub_dir

path1 = current_dir / "simple.ply"
path2 = current_dir / "mom.ply"

colors = [
    [0.5, 0.5, 0.5],  # Grey
    # [0, 1, 0],  # Green
    # [0, 0, 1],  # Red
    [0, 0, 1],  # Blue
]

file_paths = [path1, path2]

point_clouds = []
for file_path, color in zip(file_paths, colors):
    point_cloud = o3d.io.read_point_cloud(file_path.as_posix())
    point_cloud.paint_uniform_color(color)
    point_clouds.append(point_cloud)

# difference_points = np.array(point_clouds[0].points) - np.array(point_clouds[1].points)
o3d.visualization.draw_geometries(point_clouds)
# cloud = o3d.geometry.PointCloud()
# cloud.points = o3d.utility.Vector3dVector(difference_points)
# o3d.visualization.draw_geometries([cloud])
# cloud = o3d.io.read_point_cloud(path1.as_posix())
# o3d.visualization.draw_geometries([cloud])
