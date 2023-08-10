class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StoppingCriterionSingleton(metaclass=MetaSingleton):
    def __init__(self):
        self.is_memory_limit = False
        self.is_data_processed = False
        self.is_time_finished = False
        self.is_map_diverged = False
        self.is_solver_error = False

    @property
    def ON(self) -> bool:
        return any(self.__dict__.values())

    def reset(self):
        for value in self.__dict__.values():
            value = False
