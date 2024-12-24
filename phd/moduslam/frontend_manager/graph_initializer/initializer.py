import logging
from collections.abc import Iterable

from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.graph_initializer.configs import EdgeConfig
from phd.moduslam.frontend_manager.graph_initializer.distributor import (
    type_method_table,
)
from phd.utils.exceptions import ItemNotExistsError

logger = logging.getLogger(frontend_manager)


class GraphInitializer:
    """Initializes the graph with prior factors."""

    @classmethod
    def create_measurements(cls, priors: Iterable[EdgeConfig]) -> list[Measurement]:
        """Creates measurement from prior configs.

        Args:
            priors: configs with prior measurements.
        """
        measurements: list[Measurement] = []
        for prior in priors:
            m = cls._create_measurement(prior)
            measurements.append(m)

        return measurements

    @staticmethod
    def _create_measurement(config: EdgeConfig) -> Measurement:
        """Creates a new measurement for the given configuration.

        Args:
            config: a configuration for the measurement.

        Returns:
            a new measurement.

        Raises:
            ItemNotExistsError: if no method exists to create a measurement for the configuration.
        """
        try:
            create = type_method_table[config.vertex_type_name]
        except KeyError:
            msg = f"No method exists to create a measurement for the configuration {config}"
            logger.error(msg)
            ItemNotExistsError(msg)

        measurement = create(config)
        return measurement
