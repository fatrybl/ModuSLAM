from slam.utils.meta_singleton import MetaSingleton


class StoppingCriterionSingleton(metaclass=MetaSingleton):
    def __init__(self) -> None:
        self.is_memory_limit: bool = False
        self.is_data_processed: bool = False
        self.is_time_finished: bool = False
        self.is_map_diverged: bool = False
        self.is_solver_error: bool = False

    @property
    def ON(self) -> bool:
        return any(self.__dict__.values())

    def reset(self):
        for value in self.__dict__.values():
            value = False
