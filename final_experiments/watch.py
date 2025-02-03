from pathlib import Path

import open3d as o3d

# Paths to the point cloud files
current_dir = Path(__file__).parent.absolute()
sub_dir = Path("constant_speed/urban-33/output")
dir = current_dir / sub_dir

path1 = dir / "base.ply"
path2 = dir / "mom.ply"

colors = [
    [0.5, 0.5, 0.5],  # Grey
    [0, 0, 1],  # Blue
]

file_paths = [path1, path2]

point_clouds = []
for file_path, color in zip(file_paths, colors):
    point_cloud = o3d.io.read_point_cloud(file_path.as_posix())
    point_cloud.paint_uniform_color(color)
    point_clouds.append(point_cloud)

# o3d.visualization.draw_geometries(point_clouds)


cloud = o3d.io.read_point_cloud(str(path1))
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(cloud)

vis.run()
vis.destroy_window()
