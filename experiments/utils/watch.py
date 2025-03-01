from pathlib import Path

import numpy as np
import open3d as o3d
from PIL import Image


def rotate_around_x(vector, angle_deg):
    angle_rad = np.radians(angle_deg)
    rotation_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad)],
            [0, np.sin(angle_rad), np.cos(angle_rad)],
        ]
    )
    return rotation_matrix @ vector


def rotate_around_y(vector, angle_deg):
    angle_rad = np.radians(angle_deg)
    rotation_matrix = np.array(
        [
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)],
        ]
    )
    return rotation_matrix @ vector


def rotate_around_z(vector, angle_deg):
    angle_rad = np.radians(angle_deg)
    rotation_matrix = np.array(
        [
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1],
        ]
    )
    return rotation_matrix @ vector


current_dir = Path(__file__).parent.parent.absolute()
sub_dir = Path("final_experiments/")
dir = current_dir / sub_dir

path1 = dir / "base.ply"
path2 = dir / "mom.ply"
path3 = dir / "error.ply"
path4 = dir / "timeshift.ply"

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


o3d.visualization.draw_geometries(point_clouds)

vis = o3d.visualization.Visualizer()
vis.create_window(width=7680, height=4320)  # Set window size to a higher resolution

cloud = o3d.io.read_point_cloud(path2.as_posix())

vis.add_geometry(cloud)
ctr = vis.get_view_control()


# Initial front and up vectors for bird's-eye view
front = np.array([0, 0, 1])  # Camera looks upward along the Z-axis
up = np.array([0, 1, 0])  # Camera's up direction is the Y-axis

# Define rotation angles in degrees
# angle_x = 45
# angle_y = 15
# angle_z = -50
angle_x = 0
angle_y = 0
angle_z = 0

# Rotate the front and up vectors around each axis
front_rotated = rotate_around_x(front, angle_x)
front_rotated = rotate_around_y(front_rotated, angle_y)
front_rotated = rotate_around_z(front_rotated, angle_z)

up_rotated = rotate_around_x(up, angle_x)
up_rotated = rotate_around_y(up_rotated, angle_y)
up_rotated = rotate_around_z(up_rotated, angle_z)

# Set the camera parameters
ctr.set_front(front_rotated)  # Set rotated front vector
ctr.set_lookat([20, 20, 0])  # Set the camera's target position (X, Y, Z)
ctr.set_up(up_rotated)  # Set rotated up vector
ctr.set_zoom(0.4)  # Adjust the zoom level

# Run the visualizer
vis.poll_events()
vis.update_renderer()

image = vis.capture_screen_float_buffer(do_render=True)
image = np.asarray(image)
image = (image * 255).astype(np.uint8)

image_path = dir / "cloud.png"
Image.fromarray(image).save(image_path)

# Run the visualizer
vis.run()
vis.destroy_window()
