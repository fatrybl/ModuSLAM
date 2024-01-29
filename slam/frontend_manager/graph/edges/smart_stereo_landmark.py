from typing import Any, Type

import gtsam

from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.graph.edges.base_edge import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex


class SmartStereoLandmark(Edge):
    """
    Base abstract Edge of a Graph.
    """

    def __init__(self, graph: Graph, m: Any) -> None:
        self._noise_model: gtsam.noiseModel.Isotropic  # TODO: check if a model is correct
        self._vertices: tuple[Type[Vertex], ...] = ()
        self._elements: tuple[Element, ...] = ()
        self._landmark: StereoCameraLandmark = None
        self._graph = graph
        self._measurement = m
        self._K: gtsam.Cal3_S2
        self._params: gtsam.SmartProjectionParams
        self._body_P_sensor: gtsam.Pose3
        self._create()

    @property
    def gtsam_factor(self) -> gtsam.SmartProjectionPose3Factor:
        """"""

    @property
    def elements(self) -> tuple[Element, ...]:
        """
        Tuple of elements which form the edge (factor).
        Returns:
            (tuple[Element, ...]): elements without raw data.
        """
        return self._elements

    @property
    def vertices(self) -> tuple[Type[Vertex], ...]:
        """
        The vertices which are connected with an edge.

        Returns:
            (tuple[Type[Vertex], ...]): a tuple of vertices.
        """
        return self._vertices

    def _get_landmark(self, description: Any) -> Type[Vertex]:
        self._graph.vertices.stereo_landmarks.add(description)
        return self._graph.vertices.stereo_landmarks(description)

    def _create(
        self,
    ) -> None:
        self._factor = gtsam.SmartProjectionPose3Factor(
            noise=self._noise_model,
            K=self._K,
            params=self._params,
            body_P_sensor=self._body_P_sensor,
        )

        self._landmark = self._get_landmark(self._measurement)
        self._factor = self._landmark.instance
        if self._factor is None:
            self._factor = gtsam.SmartProjectionPose3Factor(
                noise=self._noise_model,
                K=self._K,
                params=self._params,
                body_P_sensor=self._body_P_sensor,
            )

        pose_id: int = self._graph.vertices.CameraPose[-1].id + 1
        self._factor.add(measured_i=self._measurement, poseKey_i=pose_id)
