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

import gtsam
import numpy as np
import PIL.Image as Image
from gtsam.symbol_shorthand import X

from moduslam.external.handlers_factory.handlers.visual_odometry.feature_detector import (
    Detector,
)
from moduslam.external.handlers_factory.handlers.visual_odometry.feature_matcher import (
    BfMatcher,
)

if __name__ == "__main__":
    img1 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00055.jpg"
    )
    img2 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00060.jpg"
    )
    img3 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00065.jpg"
    )
    img4 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00070.jpg"
    )

    camera_matrix = np.array(
        [
            [747.3121949097032, 0.0, 490.8606682225008],
            [0.0, 747.1524375957724, 505.2373814853779],
            [0.0, 0.0, 1.0],
        ]
    )
    distortion_coefficients_left = np.array(
        [
            0.019702988705266412,
            0.0019647288278805426,
            0.0020858202586604944,
            -0.0009536922337319427,
        ]
    )

    fx = camera_matrix[0, 0]
    fy = camera_matrix[1, 1]
    cx = camera_matrix[0, 2]
    cy = camera_matrix[1, 2]
    s = 0.0
    camera_model = gtsam.Cal3_S2(fx, fy, s, cx, cy)

    factors: list[gtsam.NonlinearFactor] = []
    graph = gtsam.NonlinearFactorGraph()

    tf = gtsam.Pose3()
    pose1 = gtsam.Pose3()
    pose2 = gtsam.Pose3(gtsam.Rot3(), [0.0, -0.01, 0.08])
    pose3 = gtsam.Pose3(gtsam.Rot3(), [0.02, -0.02, 0.12])
    pose4 = gtsam.Pose3(gtsam.Rot3(), [0.04, -0.05, 0.13])

    init_values = gtsam.Values()

    optimizer_params = gtsam.LevenbergMarquardtParams()
    projection_params = gtsam.SmartProjectionParams()
    projection_params.setLandmarkDistanceThreshold(20)
    camera_noise = gtsam.noiseModel.Isotropic.Sigma(2, 1)

    prior1 = gtsam.PriorFactorPose3(X(1), pose1, gtsam.noiseModel.Isotropic.Sigma(6, 0.01))
    prior2 = gtsam.PriorFactorPose3(X(2), pose2, gtsam.noiseModel.Isotropic.Sigma(6, 1))
    graph.add(prior1)
    graph.add(prior2)
    init_values.insert(X(1), pose1)
    init_values.insert(X(2), pose1)

    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, optimizer_params)
    result = optimizer.optimizeSafely()
    pose1 = result.atPose3(X(1))
    pose2 = result.atPose3(X(2))

    detector = Detector(num_features=500)
    matcher = BfMatcher()

    ##########################################################################
    # features1 = detector.get_visual_features(image1)
    # features2 = detector.get_visual_features(image2)
    # features3 = detector.get_visual_features(image3)
    # features4 = detector.get_visual_features(image4)
    #
    # keypoints1, descriptors1 = detector.get_keypoints_and_descriptors(image1)
    # descriptors1 = np.array([f.descriptor for f in features1], dtype=np.uint8)
    # keypoints2 = [f.key_point for f in features2]
    # descriptors2 = np.array([f.descriptor for f in features2], dtype=np.uint8)
    # keypoints3 = [f.key_point for f in features3]
    # descriptors3 = np.array([f.descriptor for f in features3], dtype=np.uint8)
    # keypoints4 = [f.key_point for f in features4]
    # descriptors4 = np.array([f.descriptor for f in features4], dtype=np.uint8)
    #
    # all_desc = descriptors1
    # all_keypoints = keypoints1
    # all_features = features1
    # for feature in all_features:
    #     factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, tf, projection_params)
    #     factor.add(feature.key_point.pt, X(1))
    #     factors.append(factor)
    #
    # matches = matcher.find_matches(descriptors2, all_desc)
    # matches = matcher.filter_with_ransac(keypoints2, all_keypoints, matches)
    # unmatched_features = VisualFeatureStorage.get_unmatched_features(features2, matches)
    #
    # for match in matches:
    #     f = features2[match.queryIdx]
    #     factor = factors[match.trainIdx]
    #     factor.add(f.key_point.pt, X(2))
    #
    # for feature in unmatched_features:
    #     keypoint = feature.key_point
    #     factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, tf, projection_params)
    #     factor.add(keypoint.pt, X(2))
    #     factors.append(factor)
    #
    # all_features += unmatched_features
    #
    # [graph.add(factor) for factor in factors]
    # init_values = gtsam.Values()
    # init_values.insert(X(1), pose1)
    # init_values.insert(X(2), pose2)
    # optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, optimizer_params)
    # result = optimizer.optimizeSafely()
    # pose1 = result.atPose3(X(1))
    # pose2 = result.atPose3(X(2))
    #
    # all_desc = np.array([f.descriptor for f in all_features], dtype=np.uint8)
    # all_keypoints = [f.key_point for f in all_features]
    # matches = matcher.find_matches(descriptors3, all_desc)
    # matches = matcher.filter_with_ransac(keypoints3, all_keypoints, matches)
    # unmatched_features = VisualFeatureStorage.get_unmatched_features(features3, matches)
    #
    # for match in matches:
    #     f = features3[match.queryIdx]
    #     factor = factors[match.trainIdx]
    #     factor.add(f.key_point.pt, X(3))
    #
    # for feature in unmatched_features:
    #     keypoint = feature.key_point
    #     factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, tf, projection_params)
    #     factor.add(keypoint.pt, X(3))
    #     factors.append(factor)
    #
    # all_features += unmatched_features
    #
    # [graph.add(factor) for factor in factors]
    # init_values = gtsam.Values()
    # init_values.insert(X(1), pose1)
    # init_values.insert(X(2), pose2)
    # init_values.insert(X(3), pose2)
    # optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, optimizer_params)
    # result = optimizer.optimizeSafely()
    #
    # print(result)
    # print(optimizer.error())

    # image1_array = np.array(image1)
    # image2_array = np.array(image3)
    # matched_image = cv2.drawMatches(
    #     image2_array, keypoints3, image1_array, all_keypoints, matches, None, flags=2
    # )
    # cv2.imshow("Matches", matched_image)
    # cv2.waitKey(0)

    # all_desc = np.array([f.descriptor for f in all_features])
    # all_keypoints = [f.key_point for f in all_features]
    # matches = matcher.find_matches(descriptors4, all_desc)
    # matches = matcher.filter_with_ransac(keypoints4, all_keypoints, matches)
    # unmatched_features = VisualFeatureStorage.get_unmatched_features(features4, matches)
    #
    # for match in matches:
    #     f = features4[match.queryIdx]
    #     factor = factors[match.trainIdx]
    #     factor.add(f.key_point.pt, X(4))
    #
    # for feature in unmatched_features:
    #     keypoint = feature.key_point
    #     factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, tf, projection_params)
    #     factor.add(keypoint.pt, X(4))
    #     factors.append(factor)
    #
    # all_features += unmatched_features
    #
    # for factor in factors:
    #     graph.add(factor)
    #
    # result = optimizer.optimize()
    #
    # p1 = result.atPose3(X(1)).matrix()
    # p2 = result.atPose3(X(2)).matrix()
    # p3 = result.atPose3(X(3)).matrix()
    # p4 = result.atPose3(X(4)).matrix()
    # poses = [p1, p2, p3, p4]
    #
    # print(result)
    # print(f"error: {optimizer.error()}")
    # print(f"num filtered matches: {len(matches)}")
    # print(f"num factors: {graph.nrFactors()}")
    #
    # # dot = graph.dot(result)
    # # source = Source(dot)
    # # source.render("graph", format="pdf", cleanup=True)
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
