from slam.utils.meta_singleton import MetaSingleton


class StoppingCriterionSingleton(metaclass=MetaSingleton):
    """
    High level criteria to stop mapping process. Defaults to MetaSingleton.
    """

    def __init__(self) -> None:
        self.is_memory_limit: bool = False
        self.is_data_processed: bool = False
        self.is_time_finished: bool = False
        self.is_map_diverged: bool = False
        self.is_solver_error: bool = False

    @property
    def ON(self) -> bool:
        """Checks if any of stopping criteria is active."""
        return any(self.__dict__.values())

    def reset(self):
        """resets all criteria to default values"""
        for key in self.__dict__.keys():
            self.__dict__[key] = False
