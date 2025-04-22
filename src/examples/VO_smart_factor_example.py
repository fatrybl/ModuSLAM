"""Example of using smart factors for visual odometry with TUM VIE loop-floor-0 dataset.

1. Upload 2 images.
2. Remove distortion.
3. Detect ORB features.
4. Match ORB features between the images and filter with RANSAC,
5. Draw the matches between the images (optional).
6. Create factor graph with 2 poses, add priors.
7. Add a smart factor for each matched feature.
8. Solve.
"""

# import gtsam
# import numpy as np
# import open3d as o3d
# import PIL.Image as Image
# from graphviz import Source
# from gtsam.symbol_shorthand import X

# image1 = Image.open(
#     "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00064.jpg"
# )
# image2 = Image.open(
#     "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00065.jpg"
# )
#
#
# camera_matrix = np.array(
#     [
#         [747.3121949097032, 0.0, 490.8606682225008],
#         [0.0, 747.1524375957724, 505.2373814853779],
#         [0.0, 0.0, 1.0],
#     ]
# )
# distortion_coefficients_left = np.array(
#     [
#         0.019702988705266412,
#         0.0019647288278805426,
#         0.0020858202586604944,
#         -0.0009536922337319427,
#     ]
# )
#
# detector = KeypointDetector(num_features=20)
# matcher = FeatureMatcher()
#
# image1_undistorted = detector.undistort_image(image1, camera_matrix, distortion_coefficients_left)
# image2_undistorted = detector.undistort_image(image2, camera_matrix, distortion_coefficients_left)
#
#
# fx = camera_matrix[0, 0]
# fy = camera_matrix[1, 1]
# cx = camera_matrix[0, 2]
# cy = camera_matrix[1, 2]
# s = 0.0
# camera_model = gtsam.Cal3_S2(fx, fy, s, cx, cy)
#
#
# keypoints1, descriptors1 = detector.get_orb_keypoints(image1)
# keypoints2, descriptors2 = detector.get_orb_keypoints(image2)
#
# image1_array = np.array(image1_undistorted)
# image2_array = np.array(image2_undistorted)
#
# matches = matcher.find_matches(descriptors1, descriptors2)
# matches = matcher.filter_with_ransac(list(keypoints1), list(keypoints2), matches)

# matched_image = cv2.drawMatches(
#     image1_array, keypoints1, image2_array, keypoints2, matches, None, flags=2
# )

# unmatched_keypoints1 = []
# unmatched_keypoints2 = []
#
# matched_indices1 = {m.queryIdx for m in matches}
# matched_indices2 = {m.trainIdx for m in matches}
#
# for i, kp in enumerate(keypoints1):
#     if i not in matched_indices1:
#         unmatched_keypoints1.append(kp)
#
# for i, kp in enumerate(keypoints2):
#     if i not in matched_indices2:
#         unmatched_keypoints2.append(kp)

# image1_with_unmatched = cv2.drawKeypoints(
#     image1_array, unmatched_keypoints1, None, color=(255, 0, 0)
# )
# image2_with_unmatched = cv2.drawKeypoints(
#     image2_array, unmatched_keypoints2, None, color=(255, 0, 0)
# )

# cv2.imshow("Matches", matched_image)
# cv2.waitKey(0)

# graph = gtsam.NonlinearFactorGraph()
# projection_params = gtsam.SmartProjectionParams()
#
# pose1 = gtsam.Pose3()
# pose2 = gtsam.Pose3(gtsam.Rot3(), [0.0, 0.0, 0.1])
# camera_noise = gtsam.noiseModel.Isotropic.Sigma(2, 2.0)
#
# prior1 = gtsam.PriorFactorPose3(X(1), pose1, gtsam.noiseModel.Isotropic.Sigma(6, 1))
# prior2 = gtsam.PriorFactorPose3(X(2), pose2, gtsam.noiseModel.Isotropic.Sigma(6, 10))
# graph.push_back(prior1)
# graph.push_back(prior2)
#
# for match in matches:
#     kp1 = keypoints1[match.queryIdx]
#     kp2 = keypoints2[match.trainIdx]
#
#     factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, projection_params)
#     factor.add(kp1.pt, X(1))
#     factor.add(kp2.pt, X(2))
#
#     graph.push_back(factor)
#
# graph.print()
#
#
# init_values = gtsam.Values()
# init_values.insert(X(1), pose1)
# init_values.insert(X(2), pose2)
#
# params = gtsam.LevenbergMarquardtParams()
# optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
#
# result = optimizer.optimize()
#
# p1 = result.atPose3(X(1)).matrix()
# p2 = result.atPose3(X(2)).matrix()
# poses = [p1, p2]
#
# print(result)
# print(f"error: {optimizer.error()}")
# print(f"num matches: {len(matches)}")
#
# dot = graph.dot(result)
# source = Source(dot)
# source.render("graph", format="pdf", cleanup=True)
#
# vis = o3d.visualization.Visualizer()
# vis.create_window()
#
# for pose in poses:
#     frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
#     frame.transform(pose)
#     vis.add_geometry(frame)
#
# vis.run()
# vis.destroy_window()
