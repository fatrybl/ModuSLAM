from pathlib import Path

import cv2
import numpy as np
import open3d as o3d


def calculate_camera_position(center, radius, angle_deg, height=0):
    """Compute camera position on a circular trajectory around the center point."""
    angle_rad = np.radians(angle_deg)  # Convert angle from degrees to radians
    y = center[1] + radius * np.sin(angle_rad)
    z = center[2] + radius * np.cos(angle_rad)
    return np.array([center[0] + height, y, z])


# Configuration
current_dir = Path(__file__).parent.parent.absolute()
sub_dir = Path("final_experiments/")
dir = current_dir / sub_dir

# Load point clouds (modify paths as needed)
path1 = dir / "base.ply"
path2 = dir / "mom.ply"

cloud = o3d.io.read_point_cloud(path1.as_posix())

# Set up visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(width=1920, height=1080)  # Adjust resolution as needed

vis.add_geometry(cloud)

# Add coordinate frame
coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=2.0, origin=[0, 0, 0])
vis.add_geometry(coordinate_frame)

ctr = vis.get_view_control()

# Camera trajectory parameters
center = np.array([0, 0, 0])  # Center of the point cloud
radius = 1  # Distance from center
height = 0  # Height along X-axis
num_frames = 360  # Full circle
initial_angle = 0  # Starting angle (parametrized)
fps = 30
up = np.array([0, 0, 1])

# Video writer setup
video_path = dir / "output_video.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(video_path.as_posix(), fourcc, fps, (1920, 1080))

for frame in range(num_frames):
    # Calculate current camera position
    angle = initial_angle + (frame * 360 / num_frames)
    camera_pos = calculate_camera_position(center, radius, angle, height)

    # Compute camera orientation vectors
    front = center - camera_pos
    front /= np.linalg.norm(front)

    # Update camera parameters
    ctr.set_front(front)
    ctr.set_lookat(center)
    ctr.set_up(up)
    ctr.set_zoom(0.5)  # Adjust to control field of view

    # Force render update
    vis.poll_events()
    vis.update_renderer()

    # Capture frame
    img = vis.capture_screen_float_buffer(True)
    img = np.asarray(img) * 255
    img = img.astype(np.uint8)

    # Convert to BGR for OpenCV and write frame
    video_writer.write(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # Update the visualizer window
    vis.update_geometry(cloud)
    vis.poll_events()
    vis.update_renderer()

# Cleanup
video_writer.release()
vis.destroy_window()
