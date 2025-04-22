"""Script to demonstrate the use of the SmartProjectionPose3Factor and its issues.

1. Read 2 images from TUM-VIE loop-floor-0 dataset.
2. Create a factor graph with 2 poses and add priors.
3. Detect ORB features in both images.
4. Match ORB features between the images and filter with ratio test.
"""

import cv2
import gtsam
import numpy as np
import open3d as o3d
import PIL.Image as Image
from graphviz import Source
from gtsam.symbol_shorthand import X

if __name__ == "__main__":

    image1 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00055.jpg"
    )
    image2 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00060.jpg"
    )
    image3 = Image.open(
        "/media/mark/New Volume/datasets/tum/visual_inertial_event/loop_floor_0/left_images/00065.jpg"
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

    tf = gtsam.Pose3()
    pose1 = gtsam.Pose3()
    pose2 = gtsam.Pose3(gtsam.Rot3(), [0.0, 0.0, 0.08])
    pose3 = gtsam.Pose3(gtsam.Rot3(), [0.02, 0.0, 0.12])

    init_values = gtsam.Values()
    init_values.insert(X(1), pose1)
    init_values.insert(X(2), pose2)

    params = gtsam.LevenbergMarquardtParams()
    params.setlambdaInitial(1e-1)
    params.setlambdaLowerBound(1e-2)

    graph = gtsam.NonlinearFactorGraph()
    projection_params = gtsam.SmartProjectionParams()
    camera_noise = gtsam.noiseModel.Isotropic.Sigma(2, 0.5)

    prior1 = gtsam.PriorFactorPose3(X(1), pose1, gtsam.noiseModel.Isotropic.Sigma(6, 0.01))
    prior2 = gtsam.PriorFactorPose3(X(2), pose2, gtsam.noiseModel.Isotropic.Sigma(6, 2))
    graph.add(prior1)
    graph.add(prior2)

    detector = cv2.ORB.create()
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    mask = np.ones(shape=image1.size, dtype=np.uint8) * 255
    keypoints1, descriptors1 = detector.detectAndCompute(np.array(image1), mask)
    keypoints2, descriptors2 = detector.detectAndCompute(np.array(image2), mask)
    keypoints3, descriptors3 = detector.detectAndCompute(np.array(image3), mask)

    factors = []

    for keypoint in keypoints1:
        factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, tf, projection_params)
        factor.add(keypoint.pt, X(1))
        factors.append(factor)

    matches = matcher.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    src_pts = np.array([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
    dst_pts = np.array([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 2)
    H, new_mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 0.5)
    good_matches = [m for i, m in enumerate(matches) if new_mask[i]]

    for match in good_matches:
        factor = factors[match.queryIdx]
        keypoint = keypoints2[match.trainIdx]
        factor.add(keypoint.pt, X(2))

    # for match in good_matches:
    #     factor = gtsam.SmartProjectionPose3Factor(camera_noise, camera_model, tf, projection_params)
    #     point1 = keypoints1[match.queryIdx]
    #     point2 = keypoints2[match.trainIdx]
    #     factor.add(point1.pt, X(1))
    #     factor.add(point2.pt, X(2))
    #     factors.append(factor)

    for factor in factors:
        graph.add(factor)

    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
    result = optimizer.optimizeSafely()

    p1 = result.atPose3(X(1)).matrix()
    p2 = result.atPose3(X(2)).matrix()
    poses = [p1, p2]

    print(result)
    print(f"error: {optimizer.error()}")
    print(f"num good matches: {len(good_matches)}")
    print(f"num factors: {graph.nrFactors()}")

    dot = graph.dot(result)
    source = Source(dot)
    source.render("graph", format="pdf", cleanup=True)

    vis = o3d.visualization.Visualizer()
    vis.create_window()

    for pose in poses:
        frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
        frame.transform(pose)
        vis.add_geometry(frame)

    vis.run()
    vis.destroy_window()
