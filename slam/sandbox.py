import functools
from typing import Any

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
print(result)


def multiple(func):
    @functools.wraps(func)
    def wrapper(self, item):
        func(self, item)
        for obj in self._objects:
            getattr(obj, func.__name__)(item)

    return wrapper


class Base:
    def __init__(
        self,
    ):
        self._items = []

    @property
    def items(self):
        return self._items

    def add(self, item):
        self._items.append(item)

    def remove(self, item):
        self._items.remove(item)


class SubClass(Base):
    def __init__(self, objects: tuple[Base, ...]):
        super().__init__()
        self._objects = objects

    @multiple
    def add(self, item: Any) -> None:
        super().add(item)

    @multiple
    def remove(self, item: Any) -> None:
        super().remove(item)
