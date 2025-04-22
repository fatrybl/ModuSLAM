import cv2
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
from PIL import Image

from src.moduslam.map_manager.factories.camera_pointcloud.depth_estimator import (
    DepthEstimator,
)


def undistort_image(image, camera_matrix, dist_coeffs):
    """Undistort an image and recompute the camera matrix.

    Parameters:
    image (numpy.ndarray): Input distorted image.
    camera_matrix (numpy.ndarray): Original camera matrix.
    dist_coeffs (numpy.ndarray): Distortion coefficients.

    Returns:
    undistorted_image (numpy.ndarray): Undistorted image.
    new_camera_matrix (numpy.ndarray): New camera matrix.
    """
    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, dist_coeffs, (w, h), 1, (w, h)
    )
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_image, new_camera_matrix


def depth_to_point_cloud(depth, K):
    # fx, fy = K[0, 0], K[1, 1]
    # cx, cy = K[0, 2], K[1, 2]
    #
    # height, width = depth.shape
    #
    # u = np.arange(width)
    # v = np.arange(height)
    # u, v = np.meshgrid(u, v)
    #
    # # Reproject to 3D
    # x = (u - cx) * depth / fx
    # y = (v - cy) * depth / fy
    # # z = depth / np.sqrt(x**2 + y**2 + 1)  # Normalize depth
    #
    # points = np.stack((x, y, depth), axis=-1).reshape(-1, 3)
    # return points
    # Get the image size
    h, w = depth.shape

    # Create meshgrid of pixel coordinates
    u, v = np.meshgrid(np.arange(w), np.arange(h))

    # Flatten the pixel coordinates and depth map
    u_flat = u.flatten()
    v_flat = v.flatten()
    depth_flat = depth.flatten()

    # Filter out points with zero depth
    valid = depth_flat > 0
    u_flat = u_flat[valid]
    v_flat = v_flat[valid]
    depth_flat = depth_flat[valid]

    # Camera intrinsic parameters
    fx = K[0, 0]
    fy = K[1, 1]
    cx = K[0, 2]
    cy = K[1, 2]

    # Convert depth map to 3D point cloud
    x = (u_flat - cx) * depth_flat / fx
    y = (v_flat - cy) * depth_flat / fy
    z = depth_flat

    # Stack x, y, and z coordinates
    pointcloud = np.stack((x, y, z), axis=-1)
    return pointcloud


def rectify_stereo_images(
    imgL, imgR, camera_matrix_L, camera_matrix_R, dist_coeffs_L, dist_coeffs_R, R, T
):
    """Rectify stereo images.

    Parameters:
    imgL (numpy.ndarray): Left image.
    imgR (numpy.ndarray): Right image.
    camera_matrix_L (numpy.ndarray): Camera matrix for the left camera.
    dist_coeffs_L (numpy.ndarray): Distortion coefficients for the left camera.
    camera_matrix_R (numpy.ndarray): Camera matrix for the right camera.
    dist_coeffs_R (numpy.ndarray): Distortion coefficients for the right camera.
    R (numpy.ndarray): Rotation matrix between the cameras.
    T (numpy.ndarray): Translation vector between the cameras.

    Returns:
    rectified_imgL (numpy.ndarray): Rectified left image.
    rectified_imgR (numpy.ndarray): Rectified right image.
    """
    # Get the image size
    h, w = imgL.shape[:2]

    # Compute the rectification transforms
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(
        camera_matrix_L, dist_coeffs_L, camera_matrix_R, dist_coeffs_R, (w, h), R, T, alpha=0
    )

    # Compute the rectification maps
    map1L, map2L = cv2.initUndistortRectifyMap(
        camera_matrix_L, dist_coeffs_L, R1, P1, (w, h), cv2.CV_16SC2
    )
    map1R, map2R = cv2.initUndistortRectifyMap(
        camera_matrix_R, dist_coeffs_R, R2, P2, (w, h), cv2.CV_16SC2
    )

    # Apply the rectification maps to the images
    rectified_imgL = cv2.remap(imgL, map1L, map2L, cv2.INTER_LINEAR)
    rectified_imgR = cv2.remap(imgR, map1R, map2R, cv2.INTER_LINEAR)

    return rectified_imgL, rectified_imgR


if __name__ == "__main__":
    img_left = cv2.imread(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00278.jpg",
        cv2.IMREAD_GRAYSCALE,
    )
    img_right = cv2.imread(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/right_images/00278.jpg",
        cv2.IMREAD_GRAYSCALE,
    )

    width, height = img_left.shape[::-1]
    # Intrinsic parameters for the left camera
    fx_left = 747.3121949097032
    fy_left = 747.1524375957724
    cx_left = 490.8606682225008
    cy_left = 505.2373814853779

    # Intrinsic parameters for the right camera
    fx_right = 742.5207932360779
    fy_right = 742.4219114252868
    cx_right = 494.72989356499005
    cy_right = 513.9144417615198

    # Camera intrinsic matrices
    K_left = np.array([[fx_left, 0, cx_left], [0, fy_left, cy_left], [0, 0, 1]])
    K_right = np.array([[fx_right, 0, cx_right], [0, fy_right, cy_right], [0, 0, 1]])

    # Distortion coefficients for the left camera
    k1_left, k2_left, k3_left, k4_left = (
        0.019702988705266412,
        0.0019647288278805426,
        0.0020858202586604944,
        -0.0009536922337319427,
    )

    # Distortion coefficients for the right camera
    k1_right, k2_right, k3_right, k4_right = (
        0.019143394892292526,
        0.0017469400418519364,
        0.003535762629018563,
        -0.0014236433279599385,
    )

    dist_coeffs_right = np.array([k1_right, k2_right, k3_right, k4_right])
    dist_coeffs_left = np.array([k1_left, k2_left, k3_left, k4_left])

    # SE(3) transformation matrix (4x4)
    T_lr = np.array(
        [
            [9.99957877e-01, 2.00814303e-04, -9.16651861e-03, 1.09417253e-01],
            [-1.81060018e-04, 9.99997662e-01, 2.15324322e-03, 3.06599632e-04],
            [9.16683841e-03, -2.15147900e-03, 9.99955732e-01, 7.51548808e-04],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    # Extract rotation and translation from T_lr
    R = T_lr[:3, :3]
    t = T_lr[:3, 3]

    img_left_undist, K_left_new = undistort_image(img_left, K_left, dist_coeffs_left)
    img_right_undist, K_right_new = undistort_image(img_right, K_right, dist_coeffs_right)

    # Rectify images
    rectified_left, rectified_right = rectify_stereo_images(
        img_left_undist,
        img_right_undist,
        K_left_new,
        K_right_new,
        dist_coeffs_left,
        dist_coeffs_right,
        R,
        t,
    )

    # Estimate depth
    scale = 2
    depth_est = DepthEstimator()
    depth = depth_est.estimate_depth(Image.fromarray(rectified_left))
    depth = np.maximum(depth, 1e-4)
    depth = depth / scale

    plt.imshow(depth)
    plt.show()

    # Convert depth map to point cloud with depth filtering
    points = depth_to_point_cloud(depth, K_left)

    # Convert grayscale to RGB by duplicating the grayscale values across three channels
    img_left_rgb = np.stack((img_left_undist,) * 3, axis=-1)
    depth_int = (depth * 1000).astype(np.uint16)

    color_o3d = o3d.geometry.Image(img_left_rgb)
    depth_o3d = o3d.geometry.Image(depth_int)

    rgbd_img = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color=color_o3d,
        depth=depth_o3d,
        depth_scale=1000.0,
        depth_trunc=10.0,
        convert_rgb_to_intensity=True,
    )

    # Create Open3D point cloud
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        image=rgbd_img,
        intrinsic=o3d.camera.PinholeCameraIntrinsic(width, height, K_left),
    )
    # Visualize point cloud

    points = np.asarray(pcd.points)

    # Define threshold value (example threshold)
    threshold = 2

    # Filter points based on threshold condition
    filtered_points = points[
        points[:, 2] <= threshold
    ]  # Assuming Z-axis (third column) value is used for thresholding

    # Create a new Open3D point cloud object with filtered points
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)

    # # Visualize original and filtered point clouds (optional)
    # o3d.visualization.draw_geometries([pcd, filtered_pcd])

    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd])
