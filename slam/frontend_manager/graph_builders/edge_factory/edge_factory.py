import logging
from collections import deque
from typing import Type

from slam.frontend_manager.elements_distributor import measurement
from slam.frontend_manager.elements_distributor.measurement import Measurement
from slam.frontend_manager.graph.edges import Edge, LidarOdometry, ImuOdometry
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex, Pose
from slam.frontend_manager.handlers.ABC_module import ElementHandler
from slam.frontend_manager.handlers.imu_preintegration.imu_preintegration import ImuPreintegration
from slam.frontend_manager.handlers.pointcloid_registration.pointcloud_matcher import KissICP

logger = logging.getLogger(__name__)


class EdgeFactory:
    @classmethod
    def create_edge(cls,
                    graph: Graph,
                    vertex: Vertex,
                    handler: ElementHandler,
                    measurements: deque[Measurement]) -> Type[Edge]:

        if isinstance(vertex, Pose) and isinstance(handler, KissICP):
            return LidarOdometry(vertex, measurements)
        elif isinstance(vertex, Pose) and isinstance(handler, ImuPreintegration):
            return ImuOdometry(vertex, measurements)
        else:
            msg = f'Unknown measurement type {measurement.type}'
            logger.error(msg)
            raise TypeError(msg)
