from collections import deque
from dataclasses import dataclass

import gtsam

graph = gtsam.NonlinearFactorGraph()
pose1 = gtsam.gtsam.Pose2(0, 0, 0)
pose2 = gtsam.gtsam.Pose2(1, 0, 0)
prior_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.001, 0.001, 0.001])
odom_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.05, 0.05, 0.01])
# graph.addPriorPose2(0, pose1, prior_noise)
graph.add(gtsam.BetweenFactorPose2(0, 1, gtsam.gtsam.Pose2(0.95, 0.05, 0.05), odom_noise))
graph.add(gtsam.BetweenFactorPose2(1, 2, gtsam.gtsam.Pose2(0.95, 0.05, 0.05), odom_noise))
graph.add(gtsam.BetweenFactorPose2(2, 3, gtsam.gtsam.Pose2(0.95, 0.05, 0.05), odom_noise))

init_values = gtsam.Values()
init_values.insert_pose2(0, gtsam.gtsam.Pose2(0, 0, 0))
init_values.insert_pose2(1, gtsam.gtsam.Pose2(0, 0, 0))
init_values.insert_pose2(2, gtsam.gtsam.Pose2(0, 0, 0))
init_values.insert_pose2(3, gtsam.gtsam.Pose2(0, 0, 0))
params = gtsam.LevenbergMarquardtParams()
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
result = optimizer.optimizeSafely()
# print(result)


@dataclass
class Test:
    start: int
    stop: int


t1 = Test(1, 2)
t2 = Test(1, 2)
t3 = Test(1, 3)
t4 = Test(1, 4)
t5 = Test(1, 5)
t6 = Test(1, 6)


def is_empty(d) -> bool:
    """Checks if the storage is empty."""
    return not bool(d)


states: deque[str] = deque()
# test = {}
# t_max = max(max(t.stop for t in value) for key, value in test.items())
assert states, "Empty graph candidate."
