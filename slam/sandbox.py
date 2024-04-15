import functools
import time
from pathlib import Path

import gtsam
import open3d as o3d
from gtsam.symbol_shorthand import X

from slam.data_manager.factory.readers.kaist.measurement_collector import (
    MeasurementCollector,
)


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), run_time))
        return value

    return wrapper


graph = gtsam.NonlinearFactorGraph()
pose1 = gtsam.gtsam.Pose3()
pose2 = gtsam.gtsam.Pose3()
prior_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
odom_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
# graph.addPriorPose3(X(0), pose1, prior_noise)
graph.add(
    gtsam.BetweenFactorPose3(X(0), X(1), gtsam.gtsam.Pose3(r=gtsam.Rot3(), t=[1, 0, 0]), odom_noise)
)
# graph.add(
#     gtsam.BetweenFactorPose3(X(1), X(2), gtsam.gtsam.Pose3(r=gtsam.Rot3(), t=[1, 0, 0]), odom_noise)
# )
# graph.add(
#     gtsam.BetweenFactorPose3(X(2), X(3), gtsam.gtsam.Pose3(r=gtsam.Rot3(), t=[1, 0, 0]), odom_noise)
# )
# graph.addPriorPose2(X(3), gtsam.gtsam.Pose2(3, 0.05, 0.05), prior_noise)

init_values = gtsam.Values()
init_values.insert_pose3(X(0), gtsam.gtsam.Pose3())
init_values.insert_pose3(X(1), gtsam.gtsam.Pose3())
# init_values.insert_pose3(X(2), gtsam.gtsam.Pose3())
# init_values.insert_pose3(X(3), gtsam.gtsam.Pose3())
params = gtsam.LevenbergMarquardtParams()
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
result = optimizer.optimizeSafely()


data = MeasurementCollector.read_bin(
    Path(
        "/home/mark/Desktop/PhD/mySLAM/tests_data/kaist_urban30_gangnam/VLP_left/1544676777116478000.bin"
    )
)

K = len(data) // 4  # Calculate the number of rows in the resulting matrix
matrix = data.reshape((K, 4))

# Convert NumPy array to Open3D point cloud object
# Extracting the (x, y, z) coordinates and intensity values
points_xyz = matrix[:, :3]
intensity = matrix[:, 3]

# Convert the NumPy array to an Open3D point cloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points_xyz)
# pcd.colors = o3d.utility.Vector3dVector(
#     np.tile(intensity[:, np.newaxis], (1, 3))
# )  # Assigning colors based on intensity

# Visualize the point cloud using Open3D's visualization module
o3d.visualization.draw_geometries([pcd])
