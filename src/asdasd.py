import numpy as np

# Transformation from camera to IMU
T_cam_to_imu = np.array(
    [
        [0.00671209, -0.00971447, 0.99993029, 0.14118513],
        [-0.99993865, -0.00887635, 0.00662591, 0.1552482],
        [0.00881136, -0.99991342, -0.00977345, 0.01917531],
        [0.0, 0.0, 0.0, 1.0],
    ]
)

# Transformation from camera to LiDAR
T_cam_to_lidar = np.array(
    [
        [0.016401767702498, -0.010112948899873, 0.999814337905184, 0.128861294507233],
        [-0.999053252579189, -0.040462795913874, 0.015980008065579, 0.196875730840019],
        [0.040293678501436, -0.999129866639658, -0.010767035870758, -0.126632260291528],
        [0.0, 0.0, 0.0, 1.0],
    ]
)

# Invert the transformation from camera to IMU
T_imu_to_cam = np.linalg.inv(T_cam_to_imu)

# Compute the transformation from IMU to LiDAR
T_imu_to_lidar = np.dot(T_imu_to_cam, T_cam_to_lidar)

print("Transformation from IMU to LiDAR:")
print(T_imu_to_lidar)
