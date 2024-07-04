import cv2
from matplotlib import pyplot as plt
from PIL import Image

from moduslam.frontend_manager.handlers.visual_odometry.depth_estimator import (
    DepthEstimator,
)

# Load stereo images
img_left = cv2.imread(
    "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00200.jpg",
    cv2.IMREAD_GRAYSCALE,
)
img_right = cv2.imread(
    "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/right_images/00200.jpg",
    cv2.IMREAD_GRAYSCALE,
)

depth_est = DepthEstimator()

depth = depth_est.estimate_depth(Image.fromarray(img_left))

plt.imshow(depth)  # Hide axes for better visualization
plt.show()
# # Intrinsic parameters for the left camera
# fx_left = 747.3121949097032  # Example value for focal length in x-axis in pixels
# fy_left = 747.1524375957724  # Example value for focal length in y-axis in pixels
# cx_left = 490.8606682225008  # Principal point x-coordinate (example value)
# cy_left = 505.2373814853779  # Principal point y-coordinate (example value)
#
# # Intrinsic parameters for the right camera
# fx_right = 742.5207932360779  # Example value for focal length in x-axis in pixels
# fy_right = 742.4219114252868  # Example value for focal length in y-axis in pixels
# cx_right = 494.72989356499005  # Principal point x-coordinate (example value)
# cy_right = 513.9144417615198  # Principal point y-coordinate (example value)
#
# # Camera intrinsic matrices
# K_left = np.array([[fx_left, 0, cx_left], [0, fy_left, cy_left], [0, 0, 1]])
#
# K_right = np.array([[fx_right, 0, cx_right], [0, fy_right, cy_right], [0, 0, 1]])
#
# k1_left, k2_left, k3_left, k4_left = (
#     0.019702988705266412,
#     0.0019647288278805426,
#     0.0020858202586604944,
#     -0.0009536922337319427,
# )
# k1_right, k2_right, k3_right, k4_right = (
#     0.019143394892292526,
#     0.0017469400418519364,
#     0.003535762629018563,
#     -0.0014236433279599385,
# )
#
# # Distortion coefficients for the left camera (k1, k2, k3, k4)
# dist_coeffs_left = np.array([k1_left, k2_left, k3_left, k4_left])
#
# # Distortion coefficients for the right camera (k1, k2, k3, k4)
# dist_coeffs_right = np.array([k1_right, k2_right, k3_right, k4_right])
#
# # SE(3) transformation matrix (4x4)
# T_lr = np.array(
#     [
#         [9.99957877e-01, 2.00814303e-04, -9.16651861e-03, 1.09417253e-01],
#         [-1.81060018e-04, 9.99997662e-01, 2.15324322e-03, 3.06599632e-04],
#         [9.16683841e-03, -2.15147900e-03, 9.99955732e-01, 7.51548808e-04],
#         [0.0, 0.0, 0.0, 1.0],
#     ]
# )
#
# # Step 2: Detect ORB features and compute descriptors
# orb = cv2.ORB.create()
# keypoints_left, descriptors_left = orb.detectAndCompute(img_left, None)
# keypoints_right, descriptors_right = orb.detectAndCompute(img_right, None)
#
# # Step 3: Undistort keypoints
# # Convert keypoints to numpy array
# points_left = np.array([kp.pt for kp in keypoints_left], dtype=np.float32)
# points_right = np.array([kp.pt for kp in keypoints_right], dtype=np.float32)
#
# # Undistort the points for left and right cameras
# points_left_undistorted = cv2.undistortPoints(points_left, K_left, dist_coeffs_left, None, K_left)
# points_right_undistorted = cv2.undistortPoints(
#     points_right, K_right, dist_coeffs_right, None, K_right
# )
#
# # Step 4: Match features between stereo images
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# matches = bf.match(descriptors_left, descriptors_right)
# matches = sorted(matches, key=lambda x: x.distance)
#
# # Extract matched keypoints after undistortion
# matched_points_left = np.float32([points_left_undistorted[m.queryIdx, 0] for m in matches])
# matched_points_right = np.float32([points_right_undistorted[m.trainIdx, 0] for m in matches])
#
# # Step 5: Extract baseline from SE(3) transformation
# # The translation component is the last column of the matrix, excluding the last element
# translation_vector = T_lr[:3, 3]
# baseline = np.linalg.norm(translation_vector)
#
# # Step 6: Calculate disparity
# disparities = matched_points_left[:, 0] - matched_points_right[:, 0]
#
# # Step 7: Calculate depth and triangulate 3D points
# depths = (
#     fx_left * baseline / (disparities + 1e-6)
# )  # Use fx from left camera and avoid division by zero
#
# # Compute 3D points
# points_3d = np.zeros((len(matched_points_left), 3))
# points_3d[:, 0] = (matched_points_left[:, 0] - cx_left) * depths / fx_left
# points_3d[:, 1] = (matched_points_left[:, 1] - cy_left) * depths / fy_left
# points_3d[:, 2] = depths
#
# # Step 1: Draw matches
# img_matches = cv2.drawMatches(
#     img_left,
#     keypoints_left,
#     img_right,
#     keypoints_right,
#     matches,
#     None,
#     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
# )
#
# # Step 2: Visualize depth values on the left image
# for i, point in enumerate(matched_points_left):
#     depth = depths[i]
#     text = f"{depth:.2f}"
#     point = tuple(np.int32(point))
#     cv2.circle(img_left, point, 5, (0, 255, 0), -1)  # Draw a circle for each feature point
#     cv2.putText(
#         img_left,
#         text,
#         (point[0] + 5, point[1] + 5),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (255, 255, 255),
#         1,
#         cv2.LINE_AA,
#     )
#
# # Display the images
# cv2.imshow("Matched Features with Depths", img_left)
# cv2.imshow("Matches", img_matches)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
