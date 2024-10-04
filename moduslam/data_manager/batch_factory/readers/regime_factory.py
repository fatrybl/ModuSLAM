from moduslam.system_configs.data_manager.batch_factory.regimes import (
    DataRegimeConfig,
    Stream,
    TimeLimit,
)
from moduslam.utils.auxiliary_methods import to_float, to_int


class Factory:
    """Parses regime config and create regimes for different datasets."""

    @staticmethod
    def kaist_regime(regime_config: DataRegimeConfig) -> Stream | TimeLimit:
        """Creates a regime for Kaist Urban Dataset reader.

        Args:
            regime_config: config with data flow regime.

        Returns:
            a regime.

        Raises:
            ValueError: if a regime name in config is invalid.
        """

        match regime_config.name:
            case Stream.name:
                return Stream()

            case TimeLimit.name:
                start = to_int(regime_config.start)
                stop = to_int(regime_config.stop)
                return TimeLimit(start, stop)

            case _:
                msg = "Invalid regime name in config."
                raise ValueError(msg)

    @staticmethod
    def tum_vie_regime(regime_config: DataRegimeConfig) -> Stream | TimeLimit:
        """Creates a regime for Tum Vie Dataset reader.

        Args:
            regime_config: config with data flow regime.

        Returns:
            a regime.

        Raises:
            ValueError: if a regime name in config is invalid.
        """

        match regime_config.name:
            case Stream.name:
                return Stream()

            case TimeLimit.name:
                start = to_float(regime_config.start)
                stop = to_float(regime_config.stop)
                return TimeLimit(start, stop)

            case _:
                msg = "Invalid regime name in config."
                raise ValueError(msg)

    @staticmethod
    def ros2_regime(regime_config: DataRegimeConfig) -> Stream | TimeLimit:
        """Creates a regime for ROS2 Dataset reader.

        Args:
            regime_config: config with data flow regime.

        Returns:
            a regime.

        Raises:
            ValueError: if a regime name in config is invalid.
        """

        match regime_config.name:
            case Stream.name:
                return Stream()

            case TimeLimit.name:
                start = to_int(regime_config.start)
                stop = to_int(regime_config.stop)
                return TimeLimit(start, stop)

            case _:
                msg = "Invalid regime name in config."
                raise ValueError(msg)
