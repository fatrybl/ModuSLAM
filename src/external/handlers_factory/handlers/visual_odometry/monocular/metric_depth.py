import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForDepthEstimation

from src.custom_types.numpy import MatrixMxN


class DepthEstimator:
    def __init__(self, model: str = "vitb", max_depth: float = 10):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = "depth-anything/Depth-Anything-V2-Base-hf"
        self._image_processor = AutoImageProcessor.from_pretrained(model)
        self._model = AutoModelForDepthEstimation.from_pretrained(
            model, depth_estimation_type="metric", max_depth=max_depth
        )
        self._device = device
        self._model.to(device).eval()

    def estimate_depth(self, image: Image.Image) -> MatrixMxN:
        """Estimates depth from the image and visualizes the depth map.

        Args:
            image: image to estimate depth from.

        Returns:
            estimated depth.
        """
        # Convert grayscale image to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Prepare image for the model
        inputs = self._image_processor(images=image, return_tensors="pt").to(self._device)

        with torch.no_grad():
            outputs = self._model(**inputs)

        # Interpolate to original size and visualize the prediction
        post_processed_output = self._image_processor.post_process_depth_estimation(
            outputs,
            target_sizes=[(image.height, image.width)],
        )

        predicted_depth = post_processed_output[0]["predicted_depth"]
        depth = predicted_depth.detach().cpu().numpy()

        # Visualize the depth map
        plt.imshow(depth)
        plt.colorbar()
        plt.show()

        return depth

    def generate_point_cloud(
        self, image: Image.Image, depth: MatrixMxN, focal_length_x: float, focal_length_y: float
    ) -> o3d.geometry.PointCloud:
        """Generates a 3D point cloud from the image and depth map.

        Args:
            image: original image.
            depth: depth map.
            focal_length_x: focal length along the x-axis.
            focal_length_y: focal length along the y-axis.

        Returns:
            point cloud.
        """
        width, height = image.size

        # Resize depth prediction to match the original image size
        resized_pred = Image.fromarray(depth).resize((width, height), Image.NEAREST)

        # Generate mesh grid and calculate point cloud coordinates
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        x = (x - width / 2) / focal_length_x
        y = (y - height / 2) / focal_length_y
        z = np.array(resized_pred)
        points = np.stack((np.multiply(x, z), np.multiply(y, z), z), axis=-1).reshape(-1, 3)

        # Create the point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        return pcd

    def visualize_point_cloud(self, pcd: o3d.geometry.PointCloud):
        """Visualizes the point cloud with coordinate axes at the origin.

        Args:
            pcd: point cloud to visualize.
        """
        # Create coordinate axes
        axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])

        # Visualize point cloud with coordinate axes
        o3d.visualization.draw_geometries([pcd, axes])


# Example usage
image = Image.open(
    "/media/mark/WD/tum/visual_inertial_event/test_loop_floor_0/left_images/00051.jpg"
)

estimator = DepthEstimator()
depth = estimator.estimate_depth(image)
pcd = estimator.generate_point_cloud(
    image, depth, focal_length_x=747.3121949097032, focal_length_y=747.1524375957724
)
estimator.visualize_point_cloud(pcd)
