from pathlib import Path

import open3d as o3d

current_dir = Path(__file__).parent.absolute()
# Define the file paths
path1 = current_dir / "error.ply"
path2 = current_dir / "timeshift.ply"
path3 = current_dir / "mom.ply"

# Define colors for each point cloud
colors = [
    [1, 0, 0],  # Red
    [0, 1, 0],  # Green
    # [0, 0, 1],  # Blue
]

# Define the file paths
file_paths = [path1, path2]

# Read and colorize point clouds
point_clouds = []
for file_path, color in zip(file_paths, colors):
    point_cloud = o3d.io.read_point_cloud(file_path.as_posix())
    point_cloud.paint_uniform_color(color)
    point_clouds.append(point_cloud)

# o3d.visualization.draw_geometries(point_clouds)

cloud = o3d.io.read_point_cloud(path1.as_posix())
o3d.visualization.draw_geometries([cloud])
