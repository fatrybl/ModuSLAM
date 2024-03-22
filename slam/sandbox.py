import functools
import time

import gtsam
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
pose1 = gtsam.gtsam.Pose2(0, 0, 0)
pose2 = gtsam.gtsam.Pose2(1, 0, 0)
prior_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.001, 0.001, 0.001])
odom_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.05, 0.05, 0.01])
graph.addPriorPose2(X(0), pose1, prior_noise)
graph.add(gtsam.BetweenFactorPose2(X(0), X(1), gtsam.gtsam.Pose2(0.95, 0.05, 0.05), odom_noise))
graph.add(gtsam.BetweenFactorPose2(X(1), X(2), gtsam.gtsam.Pose2(0.95, 0.05, 0.05), odom_noise))
graph.add(gtsam.BetweenFactorPose2(X(2), X(3), gtsam.gtsam.Pose2(0.95, 0.05, 0.05), odom_noise))
# graph.addPriorPose2(X(3), gtsam.gtsam.Pose2(3, 0.05, 0.05), prior_noise)

init_values = gtsam.Values()
init_values.insert_pose2(X(0), gtsam.gtsam.Pose2(0, 0, 0))
init_values.insert_pose2(X(1), gtsam.gtsam.Pose2(0, 0, 0))
init_values.insert_pose2(X(2), gtsam.gtsam.Pose2(0, 0, 0))
init_values.insert_pose2(X(3), gtsam.gtsam.Pose2(0, 0, 0))
params = gtsam.LevenbergMarquardtParams()
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
result = optimizer.optimizeSafely()


# from gtsam.gtsam import SmartProjectionPose3Factor as SmartFactor
#
# f = SmartFactor(gtsam.noiseModel.Diagonal.Sigmas([1, 1, 1]), gtsam.Cal3_S2())
# f.add([1, 1], 0)
# f.add([2, 2], 1)
# graph.add(f)

# optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
# result = optimizer.optimizeSafely()
# graph.remove(graph.nrFactors() - 1)
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
result = optimizer.optimizeSafely()
print(gtsam.imuBias.ConstantBias())


# graph.saveGraph("graph.dot", result)
#
# import pygraphviz as pgv
#
# A = pgv.AGraph("graph.dot")
# A.draw("graph.png", prog="dot")
