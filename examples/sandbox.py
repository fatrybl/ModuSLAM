import functools
import time

import gtsam
from graphviz import Source
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

init_values = gtsam.Values()
pose1 = gtsam.gtsam.Pose3()
pose2 = gtsam.gtsam.Pose3()

init_values.insert_pose3(X(0), pose1)
init_values.insert_pose3(X(1), pose2)

prior_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
odom_noise = gtsam.gtsam.noiseModel.Diagonal.Sigmas([0.05, 0.05, 0.05, 0.05, 0.05, 0.05])

graph.addPriorPose3(X(0), pose1, prior_noise)

odom = gtsam.BetweenFactorPose3(X(0), X(1), pose2, odom_noise)

graph.add(odom)

# k = gtsam.gtsam.Cal3_S2()
# smart_f1 = gtsam.gtsam.SmartProjectionPose3Factor(odom_noise, k)
# smart_f1.add(np.array([1, 1]), X(0))
# smart_f2 = gtsam.gtsam.SmartProjectionPose3Factor(odom_noise, k)
# smart_f2.add(np.array([1, 1]), X(0))
# smart_f2.add(np.array([20, 20]), X(1))
# graph.push_back(smart_f1)
# print(graph)
#
# smart_f1.add(np.array([20, 20]), X(1))

params = gtsam.LevenbergMarquardtParams()
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, init_values, params)
result = optimizer.optimizeSafely()

print(graph)

dot = graph.dot(result)
source = Source(dot)
# source.render("graph", format="pdf", cleanup=True)
