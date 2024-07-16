import functools
import time

import gtsam
import numpy as np
from gtsam.symbol_shorthand import X


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
graph.addPriorPose3(X(0), pose1, prior_noise)
graph.push_back(
    gtsam.BetweenFactorPose3(X(0), X(1), gtsam.gtsam.Pose3(r=gtsam.Rot3(), t=[1, 0, 0]), odom_noise)
)

k = gtsam.gtsam.Cal3_S2()
smart_f = gtsam.gtsam.SmartProjectionPose3Factor(odom_noise, k)
smart_f.add(np.array([1, 1]), X(0))
graph.push_back(smart_f)
smart_f.add(np.array([1, 1]), X(1))
graph.push_back(smart_f)

init_values = gtsam.Values()
init_values.insert_pose3(X(0), gtsam.gtsam.Pose3())
init_values.insert_pose3(X(1), gtsam.gtsam.Pose3())

params = gtsam.LevenbergMarquardtParams()
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)

isam = gtsam.ISAM2()
isam.update(graph, init_values)
result_isam = isam.calculateEstimate()

result = optimizer.optimizeSafely()


# pcd.colors = o3d.utility.Vector3dVector(
#     np.tile(intensity[:, np.newaxis], (1, 3))
# )  # Assigning colors based on intensity

# Visualize the point cloud using Open3D's visualization module
# o3d.visualization.draw_geometries([pcd])
