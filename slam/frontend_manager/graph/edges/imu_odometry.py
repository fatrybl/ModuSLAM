import logging
from dataclasses import dataclass

import gtsam
import numpy as np
import numpy.typing as npt

from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges.edges import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


@dataclass
class ImuOdometry(Edge):
    """
    Edge for Imu pre-integration factor.
    """

    def __init__(self, graph: Graph, m: Measurement) -> None:
        self._noise_model: gtsam.noiseModel | None = None  # TODO: check if a model is correct
        self._v1: int | None = None
        self._v2: int | None = None
        self._elements: tuple[Element, ...] = m.elements
        self._graph = graph
        self._measurement = m
        self._create()

    def _set_covariance(self, m: Measurement) -> None:
        """
        Sets the covariance matrix based on measurement.
        Either constant sensor-based covariance or dynamic measurement-based one.
        Args:
            m (Measurement): an input measurement.
        """
        if m.covariance:
            self._covariance = m.covariance
        else:
            first_element: Element
            sensor: Sensor = first_element.measurement.sensor
            self._covariance = sensor.config.measurement_covariance

        self._noise_model = gtsam.noiseModel.Isotropic.Sigmas(sigmas=self._covariance)

    def _create_vertices(self) -> None:
        """
        Creates vertices for the edge.
        Returns:

        """

    @property
    def gtsam_factor(self) -> gtsam.Factor:
        if self._factor is None:
            msg = "GTSAM factor must be initialized."
            logger.error(msg)
            raise ValueError
        else:
            return self._factor

    @gtsam_factor.setter
    def gtsam_factor(self, factor: gtsam.BetweenFactorPose3) -> gtsam.Factor:
        self._factor = factor

    @property
    def elements(self) -> tuple[Element, ...]:
        return self._elements

    @property
    def v1(self) -> int:
        return self._v1

    @property
    def v2(self) -> int:
        return self._v2

    def _create(self) -> None:
        tf: npt.NDArray[np.float64] = self._measurement.values
        gtsam_tf: gtsam.Pose3 = gtsam.Pose3(mat=tf)
        v1: int = self._graph.vertices.Pose[-1].id
        v2: int = v1 + 1

        self._set_covariance(self._measurement)

        self._factor = gtsam.ImuFactor(key1=v1, key2=v2, relativePose=gtsam_tf, noiseModel=self._noise_model)

        self._create_vertices()
